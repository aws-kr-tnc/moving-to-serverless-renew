# Lab 2: CloudAlbum with 3-tier architecture and high availability

Before we go to the serverless application architecture, let's deploy our application into the High Availability Applciation Architecture environment to see the obvious differences from the host based environment and serverless environment.

So, we'll deploy the CloudAlbum application with HA(high availability) architecture in the Amazon Web Services environment.

## In this lab cover.. 

<img src=./images/lab02-eb-diagram.png width=700>

* Configure [VPC](https://aws.amazon.com/vpc/) for the HA environment. (CloudFormation template will be provided.)
* Configure [EFS](https://aws.amazon.com/efs/) for the scalable **shared storage**.
* Configure [ElasticBeanstalk](https://aws.amazon.com/elasticbeanstalk/).
  * with [RDS](https://aws.amazon.com/rds/), [ALB](https://aws.amazon.com/elasticloadbalancing/) and [AutoScaling](https://aws.amazon.com/autoscaling/). 
  * backend application will be deployed here.
* Configure [S3](https://aws.amazon.com/s3/) for static website hosting with front-end SPA.


## Prerequisites
The following **prerequisited** are required for this hands-on lab:

* AWS Console Access.
* AWS CLI configured EC2 or PC. (***AdministratorAccess*** recommended)


## TASK 1. Create your multi-az VPC

In this section, you will create an VPC with multi-az for the high availability using CloudFormation.

<img src=./images/lab02-task1-cf-diagram.png width=700>


1. Make sure the current region is Singapore (ap-souteeast-1).

    <img src=./images/lab02-task1-region.png width=700>

2. In the AWS Console, click **Services**, then click **CloudFormation** to open the CloudFormation dashboard.

 * CloudFormation new console is available. However, this guide is wrriten for previous console. 
 * If the description of the lab-guide differs from the console screen, select '**switch to the previous console**'.

    <img src=./images/lab02-task1-cf-console.png width=700>

3. Click **Create Stack** button at the top-left corner. (or click **Create new stack** at the center of page.)

4. Download the **CloudFormation** template file (network.yaml) to your local laptop.
 * Download Link : <https://raw.githubusercontent.com/aws-kr-tnc/moving-to-serverless-renew/master/resources/network.yaml>

5. On the **Select Template** page, click **Upload a template to Amazon S3**. Click **Browse...** button. Then choose ***network.yaml*** file which is downloaded previous step.

6. Click **Next** button.

7. On the **Specify Details** page. Type `workshop-vpc` for **Stack name**. 

8. Review ***Parameters*** section. You can check the CIDR address for VPC and subnets. If you want, you can modify these values your own.

9. Click **Next** button.

10. On the **Options** page, just click **Next** button. 

11. On the **Review** page, click **Create** button. 

12. About 5 minutes later, the stack creation will be completed. Check the **Status** field. You can see that the value of Satus is ***CREATE_COMPLETE***.

    <img src=./images/lab02-task1-cf-complete.png width=700>

13. Explore the ***outputs*** tab. Copy the values of ***outputs*** tab to the your notepad for later use.


## TASK 2. Create EFS

In this section, you will create an EFS for the CloudAlbum application. 

Amazon Elastic File System (Amazon EFS) provides a simple, scalable, elastic file system for Linux-based workloads for use with AWS Cloud services and on-premises resources. It is built to scale on demand to petabytes without disrupting applications, growing and shrinking automatically as you add and remove files, so your applications have the storage they need – when they need it. It is designed to provide massively parallel shared access to thousands of Amazon EC2 instances, enabling your applications to achieve high levels of aggregate throughput and IOPS with consistent low latencies. Amazon EFS is a fully managed service that requires no changes to your existing applications and tools, providing access through a standard file system interface for seamless integration.


14. In the AWS Console, click **Services**, then click **EFS** to open the EFS dashboard console.

15. Click **Create file system** button.

16. On the **Configure file system access** page, choose your VPC . You can check the name of VPC, it should contain ***moving-to-serverless***. Then you have to choose pair of **Private subnets** and please check the each Availibity Zone of subnet. 

    <img src=./images/lab02-task2-efs-1.png width=700>

17. Click **Next Step** button. You can refer to following screen capture image.



18. On the **Configure optional settings** page, type `shared-storage` for key **Name** under **Add tags** section.

19. Then click **Next Step**. (Leave the remaining configuration as default.)

20. On the **Review and create** page, check the configuration then click **Create File System** button.

21. After a while, you will see that the **Mount target state** changes from **Creating** to **Available** on the **Mount targets** section at the right-bottom corner.

22. If the **Mount target state** becomes **Available**, Copy the **File system ID** and paste it ***notepad*** for later use in TASK 5. 


* Move to the next TASK.


## TASK 3. Confiugure ElasticBeanstalk

Now, we will deploy the CloudAlbum application using ElasticBeanstalk. Our application will be  integrated EFS, Elasticache, RDS, ALB, and AutoScalingGroup via ElasticBeanstalk.

With Elastic Beanstalk, you can quickly deploy and manage applications in the AWS Cloud without having to learn about the infrastructure that runs those applications. Elastic Beanstalk reduces management complexity without restricting choice or control. You simply upload your application, and Elastic Beanstalk automatically handles the details of capacity provisioning, load balancing, scaling, and application health monitoring.

23. In the **AWS Management Console** on the **Service** menu, click **ElasticBeanstalk**.

24. At the top-right of screen, clikck **Create New Application**.

25. At the **Create New Application** window, configure the following:

* **Application Name** : `HA-CloudAlbum`
* **Description** : `Moving to AWS Serverless Workshop`

26. Click **Create** button.

27. At the **All Applications > HA-CloudAlbum** page, click the **Create one now**.

28. On the **Select environment tier**, page:

 * Select **Web server environment**. 
 
29. Click **Select** button.

30. Type domain name in **Domain** field. For example `myapp-<initial>` then click **Check Availability**.

31. In the **Create a web server environemnt** section, for **Description** type `HA-CloudAlbum`

32. In the **Base configuration** section, configure the following:

* **Preconfigured plafform** : `Python`

    <img src=./images/lab02-task4-eb-python.png width=500>

* **Application code** : ***Sample application***

33. Click **Configure more options**.

34. In the **Configure HaCloudalbum-env** page : Change the **Configuration presets** from **Low cost(Free Tier eligible)** to ***High avalability***.

 * **Configuration presets** : ***High avalability***
 
    <img src=./images/lab02-task4-eb-preset.png width=400>

 * **NOTE**: We will start from ***High availability*** preset for the convenience. We need to change some configuration for our application. 

35. In the **Database** section, click **Modify**.

 * **NOTE**: Please note that creating the database with ElasticBeanstalk ties it to the life-cycle of the ElasticBeanstalk environment. If the database is required to persistent in the event of the ElasticBeanstalk environment, We need to remove it from ElasticBeanstalk environment. We would recommend creating a RDS instance outside of ElasticBeanstalk and then connecting the ElasticBeanstalk environment to this database.
 
 * Using Elastic Beanstalk with Amazon Relational Database Service. (https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html)


36. In the **Database settings** section, configure following parameters.

 * **Username** : `movingto`
 * **Password** : `serverless`
 * **Retention** : `Delete`
 * **Availability** : `High (Multi-AZ)`

    <img src=./images/lab02-task4-eb-db.png width=500>

**NOTE:** Because it is a hands-on environment, not a real operating environment, select **'Delete'** for convenience.

37. Click **Save** button.

38. In the **Network** section, click **Modify**.

39. In the **Virtual private cloud (VPC)** section of **Modify network** page, choose a VPC which tagged 'moving-to-serverless'.

    <img src=./images/lab02-task4-eb-network.png width=500>

40. In the **Load balancer settings** section, configure followings.
 
 * **Visivility** : `Public`
 
 * Choose **Availability Zone** and **Subnet**. You can choose ***Public Subnet - 1*** and ***Public Subnet -2***

    <img src=./images/lab02-task4-eb-alb.png width=700>


41. In the **Instance settings** section, configure followings.
 
 * Choose **Availability Zone** and **Subnet**. You can choose ***Private Subnet - 1*** and ***Private Subnet -2***

    <img src=./images/lab02-task4-eb-instance.png width=700>

42. In the **Database settings** section, configure followings.
 
 * Choose **Availability Zone** and **Subnet**. You can choose ***Private Subnet - 1*** and ***Private Subnet -2***

    <img src=./images/lab02-task4-eb-dbsubnet.png width=700>

43. Click **Save** button.

44. Click **Modify** button of **Instances** section in the **Configure HaCloudalbum-env** page.

45. Choose a default security group, in the **EC2 security groups** section in the **Modify instances** page.

    <img src=./images/lab02-task4-eb-instance-sg.png width=500>

46. Click **Save** button.

47. Click **Create environment** button in the bottom of the Configure HaCloudalbum-env page.

* **NOTE:** It will probably take 15 minutes or so. It is good to drink coffee for a while.

    <img src=./images/coffee-cup.png width=200>

* <div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


## TASK 4. Deploy Application with ElasticBeanstalk

If the previous TASK was successfully completed, you will see the following screen.

<img src=./images/lab02-task5-eb-simpleapp.png  width=700> 

* You can see the deployed application by clicking on the URL link in the top line.

    <img src=./images/lab02-task5-eb-simpleapp-screen.png width=500> 

Now, let's deploy our application.


48. Setup ElasticBeanstalk configuration to deploy back-end application.  Click the **Configuration** button in the left navigation menu.

    <img src=./images/lab02-task5-eb-configuration.png width=300>

* We will change the some configuration for our application.

49. Copy the RDS **Endpoint** value to the ***notepad*** for the later use. You can find it in **Database** section. It is located bottom of the **Configuration overview** page.

    <img src=./images/lab02-task5-rds-endpoint.png width=300>

50. In the **Software** section, click **Modify** button for the environment variable configuration.

51. In the **Modify software** page, you can find  **Environment properties** section. Configure following variables.

* ***Name*** : ***Value***
* `APP_HOST` : `0.0.0.0`
* `APP_PORT` : `5000`
* `DATABASE_URL` : `mysql+pymysql://movingto:serverless@<YOUR DATABASE ENDPOINT>/ebdb?charset=utf8`
  * **NOTE**: Replace ***`<YOUR DATABASE ENDPOINT>`*** to **your own EndPoint** value which copied previous step. 
  * For example : `mysql+pymysql://movingto:serverlessp@`aa1is6q2iidf84x.cjukz33spdko.ap-southeast-1.rds.amazonaws.com:3306`/ebdb?charset=utf8`
* `EFS_ID` : `<YOUR FILE SYSTEM ID>`
  * We already copied it to notepad in **TASK 2**.
  * For example : fs-5d3e921c
* `FLASK_SECRET` : `serverless`
  * This value will be used for Flask app's SECRET_KEY.
* `UPLOAD_FOLDER` : `/mnt/efs`

    <img src=./images/lab02-task5-eb-sw-env-var-1.png width=500>

* You can check the `LAB02/backend/cloudalbum/config.py` file about above variables.


52. Click **Apply** button.


53. Click the **Configuration** button in the left navigation menu.

54. In the **Load balancer** section, click **Modify** button.

55. In the **Modify load balancer** page, Find **Processes** section then click the checkbox of ***default*** process for the application health check configuration. And click the **Actions** button, then you can choose **Edit** menu.

    <img src=./images/lab02-task5-eb-alb-health.png width=500>

56. Configure **Health check** variables.
* **HTTP code** : `200`
* **Path** : `/admin/health_check`

     <img src=./images/lab02-task5-eb-alb-health-2.png width=500>

* Here is health check logic.(backend/cloudalbum/api/admin.py)
```python
...

@api.route('/health_check')
class HealthCheck(Resource):
    @api.doc(responses={200: 'system alive!'})
    def get(self):
        try:
            # 1. Is database available?!
            db.engine.execute('SELECT 1')
            # 2. Is disk have enough free space?!
            total, used, free = shutil.disk_usage('/')
            if used / total * 100 >= 90:
                raise Exception('free disk size under 10%')
            # 3. Something else..
            # TODO: health check something
            return make_response({'ok': True, 'Message': 'Healthcheck success: {0}'.format(get_ip_addr())}, 200)
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError('Healthcheck failed: {0}: {1}'.format(get_ip_addr(), e))
...
```

57. Click **Save** button.

58. Next, click **Apply** button.


59. Let's examine `.ebextensions/cloudalbum.config` in the backend application root directory.
```yaml
packages:
  yum:
    amazon-efs-utils : []

files:
  "/app/cloudalbum/efs_setup.sh":
    mode: "000755"
    owner: root
    group: root
    content: |
      #!/bin/bash

      # Commands that will be run on containter_commmands
      # Here the container variables will be visible as environment variables.
      . /opt/elasticbeanstalk/support/envvars

      ## EFS mount
      mkdir -p /mnt/efs
      
      mountpoint /mnt/efs
      
      if [ $? -eq 0 ] ; then
        echo "Already mounted"
      
      else
        mount -t efs $EFS_ID:/ /mnt/efs
      fi

      chown -R wsgi:wsgi /mnt/efs
      chown -R wsgi:wsgi /app/cloudalbum

container_commands:
  efs_setup:
    command: /app/cloudalbum/efs_setup.sh
  01_wsgipass:
    command: 'echo "WSGIPassAuthorization On" >> ../wsgi.conf'

option_settings:
  aws:elasticbeanstalk:application:environment:
    LANG: ko_KR.UTF-8
    LC_ALL: ko_KR.UTF-8

  aws:elasticbeanstalk:container:python:
    WSGIPath: wsgi.py

```
* You can configure ElasticBeanstalk environment through `.ebextensions`.
  * Install EFS utility package.
  * Generate `efs_setup.sh` to mount EFS as a shared storage.
  * Configure `WSGIPassAuthorization On`.
    * The WSGIPassAuthorization directive can be used to control whether HTTP authorisation headers are passed through to a WSGI application in the HTTP_AUTHORIZATION variable of the WSGI application environment when the equivalent HTTP request headers are present.
  * Specifies the WSGI executable script.


60. You can use `cloudalbum-v1.0.zip` file to deploy ElasticBeanstalk. Refer to below link.
 * https://github.com/aws-kr-tnc/moving-to-serverless-renew/raw/master/resources/cloudalbum_v1.0.zip

* If you want, you can make a your own zip file using following command.
  
```console
mkdir -p ~/environment/deploy
cd ~/environment/LAB02/backend/
zip -r ~/environment/deploy/cloudalbum-v1.0.zip .
```

61. In the **Dashboard**, click **Upload and Deploy** button.

62. Click the **Browse...** button and choose `cloudalbum_v1.0.zip` file which downloaded previous step. 

    <img src=./images/lab02-task5-deploy.png width=500>

63. Click **Deploy** button. When the deployment completes successfully, you will see the **'Health OK'** message in your browser.

64. You can test the Application by calling the following URL.
 * `http://<ElasticBeanstalk URL>/admin/health_check`


65. Now, let's run following command to build front-end application.

* Before, build we need to modify `.env` file to change backend server end point. We will use ElasticBeastalk URL as a backend server end point.

* open `~/environment/frontend/cloudalbum/.env` and modify it like below.
```console
//AXIOS api request time-out
VUE_APP_TIMEOUT=15000

//For test/development api end-point
//VUE_APP_API=http://127.0.0.1:5000

//For deployment
//VUE_APP_API=http://<DEPLOYED_SERVER>

//Is using S3 presinged URL?!
VUE_APP_S3_PRESIGNED_URL=false

//For LAB04 AWS Chalice serverless framework
VUE_APP_USING_CHALICE=false

```

* Replace `<DEPLOYED_SERVER>` to your own Elastic Beanstalk URL.

66. Let's build front-end application.

```console
cd ~/environment/frontend/cloudalbum/
npm run build
```
* You can see similar messages below, if you complete the build.
```console
...
...
...
 DONE  Build complete. The dist directory is ready to be deployed.
 INFO  Check out deployment instructions at https://cli.vuejs.org/guide/deployment.html
```

67. Now, move front-end application to Amazon S3.

* We need to change default S3 block public access policy for frontend application. Check your S3 policy.

    <img src=./images/lab02-task4-s3-bucket-public.png width=500>


```console
aws s3 mb s3://cloudalbum-<your-initial>
```

* You can see the message like below
```console
make_bucket: cloudalbum-<your-initial>
```

* We will use this bucket until end of this hands-on, please copy and paste your **bucket name** into your notes pad.

* Copy front-end to S3 bucket and enable `Static website hosting`.
```console
cd ~/environment/frontend/cloudalbum/dist
aws s3 sync . s3://cloudalbum-<your-initial>/ --acl public-read
aws s3 website s3://cloudalbum-<your-initial>/ --index-document index.html
``` 

68. Connect to front-end via your browser. Here is S3 URL rule pattern.
 * `http://<BUCKET NAME>.s3-website-<REGION CODE>.amazonaws.com`

 * Currently, both backend and frontend are configured to communicate with **http**. (not https)

 * For example, if your frontend bucket name is 'frontend-1234' and the region you use is Singapore (ap-southeast-1):
   * http://frontend-1234.s3-website-ap-southeast-1.amazonaws.com

 * If everything are fine, you can see the frontend like below.

 <img src="./images/lab01-08.png" width=500>


69. Enjoy the following features of your application.

<img src=./images/lab01-02.png width=800>

* Sign in / up
* Upload Sample Photos
* Check the Photo Map
* Delete photo
* Sign out


70. If it works fine, let's change your mimimum capacity configuration. In the Configuration menu, click **Modify** button of **Capacity** section.


71. In the **Modify capacity** page, change the atttribute of AutoScalingGroup ***Min*** value from 1 to 2. (or what you want..)

    <img src=./images/lab02-task5-asg.png width=500>


72. Click the **Apply** button. let's wait until the configuration is applied.
 * We have modified our application to use Elasticache as a session store. So CloudAlbum works well in AutoScaling environment. 
 
 * **To confirm this**, we can run below script in your Cloud9 terminal.
 ```console
 watch -n 1 http http://<ElasticBeanstalk URL>/admin/health_check
 ```
or
```console
while true; do http http://<ElasticBeanstalk URL>; sleep 1; done
```

* You should replace `<ElasticBeanstalk URL>` to your own URL. You can see that the load balancer distributes traffic across two instances.


73. Test the deployed application and explore the ElasticBeastalk console. 


## TASK 5. Remove your AWS resources
**CAUTION**: If you have completed this hands-on lab so far, **please delete the AWS resources** which used in this lab. You may incur an unwanted fee.

74. Remove your EB environment (RDS, ALB, ASG included). Click the **Actions** button in your ElasticBeanstalk application dashboard and then choose **Terminate Environment**. Confirm that resources created by ElasticBeanstalk are deleted.

    <img src=./images/lab02-task7-eb-delete.png width=600 >


75. Remove your EFS. Choose your file-system(**shared-storage**) and click the **Actions** button then choose **Delete file system**. Confirm that the EFS resource has been deleted. 

    <img src=./images/lab02-task7-efs-delete.png width=500>



76. Remove your VPC from CloudFormation console. Choose your CloudFormation stack(**workshop-vpc**) and click the **Actions** button then choose **Delete Stack**. Confirm that the Stack resources has been deleted.

    <img src=./images/lab02-task7-cf-delete.png width=500>

# Congratulation! You completed LAB02.


## LAB GUIDE LINKS
* [Lab 1: CloudAlbum with 3-tier Architecture](LAB01.md)
* [Lab 2: CloudAlbum with 3-tier architecture and high availability](LAB02.md)
* [Lab 3: CloudAlbum with Serverless Architecture - Part 1](LAB03.md)
* [Lab 4: CloudAlbum with Serverless Architecture - Part 2](LAB04.md)
