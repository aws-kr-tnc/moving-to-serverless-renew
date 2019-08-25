# LAB 03 - Moving to AWS serverless
We will move the components of legacy application which has constraints of scalability and high availability to serverless environment one by one.

## TASK 1. Permission grant for Cloud9

AWS Cloud9 is configured with **AWS managed temporary credentials** as default. However we will **not use** AWS managed temporary credentials due to our application need various service such as DynamoDB, S3, Lambda and so on. We will use our own policy for this workshop.

There are two ways. One is to use [1] **Using Instance Profile** with temporary credentials and this is recommended. The other way is **Store Permanent Access Credentials** in the credential file which related administrator privileadge already you used. (You can also use environment variables as a alternative way)

* Related document : [Create and Use an Instance Profile to Manage Temporary Credentials](https://docs.aws.amazon.com/cloud9/latest/user-guide/credentials.html)

* **Choose following one** :
  * ***[1] Using Instance Profile*** 
  
      or
  
  * ***[2] Store Permanent Access Credentials***

* ***[1] Using Instance Profile*** is recommended. However If you want **quick start**, you can choose ***[2] Store Permanent Access Credentials*** with enough permission.

### [1] Using Instance Profile

### [1-1] Check the AWS credentials in Cloud9 instance.
* Run following command, then you can see the AWS managed temporary credentials.
``` console
aws configure list
```
* output
``` 
aws configure list
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************YV3J shared-credentials-file    
secret_key     ****************F240 shared-credentials-file    
    region           ap-southeast-1      config-file    ~/.aws/config
```

### [1-2] Disable AWS managed temporary credentials
<img src=./images/lab03-task0-aws-setup.png width=500>

* (1) Click the setup(gear) icon
* (2) Select ***AWS SETTINGS***.
* (3) Disable ***AWS managed temporary credentials***

* Check the AWS credentials in Cloud9 instance.
```console
aws configure list
```
* output:
```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key                <not set>             None    None
secret_key                <not set>             None    None
    region                <not set>             None    None
```

* OK, done. Move to next step.

### [1-3] Create an Instance Profile for Cloud9 instance
We will grant appropriate permissions to Cloud9 instance for application development. If you prefer to use the AWS CLI to do this, see the LINK below.

* **For CLI (local machine or EC2) users** : [CLI GUIDE (click)](LAB03-ROLE-CLI.md){:target="_blank"}.

#### Let's Start!

* You may have **AdministratorAccess** privileged aws account or IAM account.
* In AWS Console, move to **IAM** service.
* Select **Policy** menu in the left and click **Create Policy** button.

<img src=./images/lab03-task0-iam-policy.png width=600>

* Click **JSON** tab in the editor.
* Copy and paste below JSON.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "apigateway:*",
                "s3:*",
                "ec2:*",
                "cloudwatch:*",
                "logs:*",
                "iam:*",
                "ssm:*",
                "lambda:*",
                "cloud9:*",
                "dynamodb:*",
                "cognito-idp:*",
                "xray:*"
            ],
            "Resource": "*"
        }
    ]
}
```

* Click **Review Policy** in the bottom line.
* Type `workshop-cloud9-policy` in the name field and click **Create Policy** in the bottom line.
* Ok. You made the IAM policy used in the role.
* Next, you will make "assume role" with the predefined policy.
* Click **Role** in the left menu.
* Click **Create Role** button.
* Select **AWS services** in the **Select type of trusted entity** section.
* Select **EC2** in the **Choose the service that will use this role** section.

<img src=./images/lab03-task0-iam-role.png width=700>

* Click **Next Permission** button in the bottom line.
* Search **workshop-cloud9-policy** policy using **Filter policies**.
* Check the result item and click **Next: Tags** button in the bottom line.
* Click **Next: Review** button in the bottom line.
* Type `workshop-cloud9-instance-profile-role` in the name field and click **Create Role** button in the bottom line.


### [1-4] Attach an Instance Profile to Cloud9 Instance
* We will find Cloud9 EC2 instance in **AWS Management Console**
* Move to **EC2** service in AWS Management Console.
* You can find EC2 instance which name include **aws-cloud9-...**.
* Click **Actions** button and click **Instance settings**.

<img src=./images/lab03-task0-ec2-instance-profile.png width=700>

* Click **Attach/Replace IAM Role** menu.
* You can find **workshop-cloud9-instance-profile-role** in the list and select it.
* Click **Apply** button.
* Click **Close** button.



### Back to the your Cloud9 terminal.

 * Configure default region:
```console
aws configure set region ap-southeast-1
```
 * Check the configured credentials
```console
aws configure list
```
* output:
```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************LZOJ         iam-role    
secret_key     ****************hK+3         iam-role    
    region           ap-southeast-1      config-file    ~/.aws/config
```

* You can see the ***iam-role*** type of access_key and secret_key. Well done.

* Is it OK? 
  * **Go to TASK 1**

### [2] Store Permanent Access Credentials ###
**NOTE:** This is **an ALTERNATIVE WAY** of ***[1] Using Instance Profile***. If you complete ***[1] Using Instance Profile***, You can pass below steps and **go to TASK 1.**

* **NOTE:** Before you proceed, please complet following steps:
  * [1-1] Check the AWS credentials in Cloud9 instance.
  * [1-2] You must disable AWS managed temporary credentials


* Configure your own credentials:
```console
aws configure set aws_access_key_id <YOUR OWN ACCESS KEY ID>
aws configure set aws_secret_access_key <YOUR OWN ACCESS KEY ID>
aws configure set region ap-southeast-1
```

* OK, all things are done. Go to TASK 1.

* **ALTERNATIVE**: You can configure following variables before run application or CLI commands. ***AdministratorAccess*** privilege is recommended. (refer to above ***workshop-cloud9-policy.json***.)
***export AWS_ACCESS_KEY_ID=<YOUR OWN ACCESS KEY ID\>*** and ***export AWS_SECRET_ACCESS_KEY=<YOUR OWN ACCESS KEY ID\>***


## TASK 2. Go to DynamoDB
Amazon [DynamoDB](https://aws.amazon.com/dynamodb/) is a nonrelational database that delivers reliable performance at any scale. It's a fully managed, multi-region, multi-master database that provides consistent single-digit millisecond latency, and offers built-in security, backup and restore, and in-memory caching.

In this TASK, we will introduce DynamoDB for CloudAlbum application. We also introduce pynamodb which is a Pythonic interface to Amazon’s DynamoDB. By using simple, yet powerful abstractions over the DynamoDB API. It is similar to SQLAlchemy.


* Leagacy application uses RDBMS(MySQL), we will replace it to DynamoDB. DynamoDB is fully managed service.It means that automatically scales throughput up or down, and continuously backs up your data for protection.
<img src=./images/lab03-task1-ddb.png width=600>

* Legacy application uses **SQLAlchemy** for OR-Mapping. SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
  * visit : https://www.sqlalchemy.org/

* We will use **PynamoDB** instead of **SQLAlchemy** for OR-Mapping of DynamoDB. It is similar with SQLAlchemy. PynamoDB is a Pythonic interface to Amazon’s DynamoDB. By using simple, yet powerful abstractions over the DynamoDB API, PynamoDB allows you to start developing immediately.
  * visit : https://github.com/pynamodb/PynamoDB

* Legacy application has simple data model and we can design DynamoDB table easily.
  <img src=./images/lab03-task1-modeling.png width=600>

1. Install required Python packaged:
```console
sudo pip-3.6 install -r ~/environment/moving-to-serverless-workshop-1d/LAB03/01-DDB/requirements.txt
```


2. Open the **model_ddb.py** which located in  '**LAB03/01-DDB**/backend/cloudalbum/database/model_ddb.py'.

3. Review the data model definition via **SQLAlchemy**. **User** table and **Photo** table are inherited from SQLAlchemy's **db.Model** and are represented in **Python classes**.

```python
from flask_login import UserMixin
from sqlalchemy import Float, DateTime, ForeignKey, Integer, String
from datetime import datetime
from cloudalbum import db

class User(UserMixin, db.Model):
    """
    Database Model class for User table
    """
    __tablename__ = 'User'

    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(100), unique=True)
    username = db.Column(String(50), unique=False)
    password = db.Column(String(100), unique=False)

    photos = db.relationship('Photo',
                             backref='user',
                             cascade='all, delete, delete-orphan')


class Photo(db.Model):
    """
    Database Model class for Photo table
    """
    __tablename__ = 'Photo'

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey(User.id))
    tags = db.Column(String(400), unique=False)
    desc = db.Column(String(400), unique=False)
    filename_orig = db.Column(String(400), unique=False)
    filename = db.Column(String(400), unique=False)
    filesize = db.Column(Integer, unique=False)
    geotag_lat = db.Column(Float, unique=False)
    geotag_lng = db.Column(Float, unique=False)
    upload_date = db.Column(DateTime, unique=False)
    taken_date = db.Column(DateTime, unique=False)
    make = db.Column(String(400), unique=False)
    model = db.Column(String(400), unique=False)
    width = db.Column(String(400), unique=False)
    height = db.Column(String(400), unique=False)
    city = db.Column(String(400), unique=False)
    nation = db.Column(String(400), unique=False)
    address = db.Column(String(400), unique=False)


```

4. Open the **models_ddb.py** which located in  'LAB03/01-DDB/backend/cloudalbum/model/models_ddb.py'.
<img src=./images/lab03-task1-models_ddb-2.png width=300>



5. Review the data model definition via **PynamoDB**. This will show how DynamoDB tables and GSI are defined in PynamoDB. They are all expressed in **Python Class.**

```python
from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, ListAttribute, MapAttribute
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection

from tzlocal import get_localzone

from cloudalbum.util.config import conf


class EmailIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = 'user-email-index'
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(['password'])

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    email = UnicodeAttribute(hash_key=True)


class User(Model):
    """
    User table for DynamoDB
    """

    class Meta:
        table_name = 'User'
        region = conf['AWS_REGION']

    id = UnicodeAttribute(hash_key=True)
    email_index = EmailIndex()
    email = UnicodeAttribute(null=False)
    username = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)


class Photo(Model):
    """
    Photo table for DynamoDB
    """

    class Meta:
        table_name = 'Photo'
        region = conf['AWS_REGION']

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    tags = UnicodeAttribute(null=True)
    desc = UnicodeAttribute(null=True)
    filename_orig = UnicodeAttribute(null=True)
    filename = UnicodeAttribute(null=True)
    filesize = NumberAttribute(null=True)
    geotag_lat = UnicodeAttribute(null=True)
    geotag_lng = UnicodeAttribute(null=True)
    upload_date = UTCDateTimeAttribute(default=datetime.now(get_localzone()))
    taken_date = UTCDateTimeAttribute(null=True)
    make = UnicodeAttribute(null=True)
    model = UnicodeAttribute(null=True)
    width = UnicodeAttribute(null=True)
    height = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)
    nation = UnicodeAttribute(null=True)
    address = UnicodeAttribute(null=True)
```

6. Review the **__init__.py** in the database package. The DynamoDB **User** and **Photo** tables will be **created automatically** for the convenience. **Note** the **(Model).create_table** function which used in **LAB03/01-DDB/backend/cloudalbum/database/__init__.py**. This is a feature of Pynamodb Model class.

```python
from flask import currenct_app as app
from cloudalbum.database.model_ddb import User
from cloudalbum.database.model_ddb import Photo


if not User.exists():
    User.create_table(read_capacity_units=app.config['DDB_RCU'], write_capacity_units=app.config['DDB_WCU'], wait=True)
    app.logger.debug('DynamoDB User table created!')

if not Photo.exists():
    User.create_table(read_capacity_units=app.config['DDB_RCU'], write_capacity_units=app.config['DDB_WCU'], wait=True)
    app.logger.debug('DynamoDB User table created!')
```

7. Review the 'LAB03/01-DDB/backend/cloudalbum/config.py' file. **New attributes** are added for DynamoDB.

* The second parameter of **os.getenv** function is the default value to use when the first parameter does not exist.

```python
import os

class BaseConfig:
	(.. ..)
	
    AWS_REGION = os.getenv('AWS_REGION', 'ap-southeast-1')
    DDB_RCU = os.getenv('DDB_RCU', 10)
    DDB_WCU = os.getenv('DDB_WCU', 10)

```
* For provisioned mode tables, you specify throughput capacity in terms of Read Capacity Units (RCU) and Write Capacity Units(WCU).
	* visit : https://docs.aws.amazon.com/ko_kr/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html

### TODO #1

8. Find **TODO #1** in the 'LAB03/01-DDB/backend/cloudalbum/api/users.py' file and please implement your own code instead of using following solution function which name is **solution\_put\_new\_user** for user signup.



```python
	if not exist_user:
	    new_user_id = uuid.uuid4().hex
	
	    # TODO 1 : Implement following solution code to save user information into DynamoDB
	    solution_put_new_user(new_user_id, user_data)
	
	    user = {
	        "id": new_user_id,
	        'username': user_data['username'],
	        'email': email
	    }
```

**NOTE**: The partition key value of User table used **uuid.uuid4().hex** for the appropriate key distribution.

* At **solution\_put\_new\_user** function, you can find how to put item with **User** table which is defined at LAB03/01-DDB/backend/cloudalbum/database/model_ddb.py with Pynamodb Model class.

```python 
	user = User(new_user_id)
	user.email = user_data['email']
	user.password = generate_password_hash(user_data['password'])
	user.username = user_data['username']
	user.save()

```



### TODO #2 

9. Find **TODO #2** in the 'LAB03/01-DDB/backend/cloudalbum/api/users.py' file and please implement your own code instead of following solution function which name is **solution_get_user_data_with_idx** for user signin feature.

```python
	signin_data = validate_user(req_data)['data']
	
	# TODO 2: Implement following solution code to get user profile with GSI
	db_user = solution_get_user_data_with_idx(signin_data)
	
	if db_user is None:
	    return m_response(False, {'msg':'not exist email', 'user':signin_data}, 400)
```
* Above solution code shows the way of using GSI which has a partition key as email.

* Inside of **solution\_get\_user\_data\_with\_idx** function, you can find how to query to GSI **email_index**, which is defined at LAB03/01-DDB/backend/cloudalbum/database/model_ddb.py.

```python
    for user_email in User.email_index.query(signin_data['email']):
        if user_email is None:
            return None
        return user_email

```


### TODO #3

10. Find **TODO #3** in the 'LAB03/01-DDB/backend/cloudalbum/api/photos.py' file and please implement your own code instead of following solution function which name is **solution\_put\_photo\_info\_ddb** to put item into Photo table.

```python
	# TODO 3: Implement following solution code to put item into Photo table of DynamoDB
	solution_put_photo_info_ddb(user_id, filename, form, filesize)
```

* Inside of **solution\_put\_photo\_info\_ddb**, you can find how to put item into DynamoDB with Pynamodb. Just fill your data into Photo model, then *save()* it. 

```python
	new_photo = Photo(id=filename,
              user_id=user_id,
              filename=filename,
              filename_orig=form['file'].filename,
              filesize=filesize,
              upload_date=datetime.today(),
              tags=form['tags'],
              desc=form['desc'],
              geotag_lat=form['geotag_lat'],
              geotag_lng=form['geotag_lng'],
              taken_date=datetime.strptime(form['taken_date'], "%Y:%m:%d %H:%M:%S"),
              make=form['make'],
              model=form['model'],
              width=form['width'],
              height=form['height'],
              city=form['city'],
              nation=form['nation'],
              address=form['address'])
     new_photo.save()
```

### TODO #4 

11. Find **TODO #4** in the 'LAB03/01-DDB/backend/cloudalbum/api/photos.py' file and please implement your own code instead of following solution function which name is **solution\_delete\_photo\_from\_ddb** to delete item from Photo table.

```python
	# TODO 4: Implement following solution code to delete a photo from Photos which is a list
	filename = solution_delete_photo_from_ddb(user, photo_id)
```

* Inside of **solution\_delete\_photo\_from\_ddb** function, you can find how to delete an item from Photo table with Pynamodb api.

```python
	photo = Photo.get(user['user_id'], photo_id)
	photo.delete()
```

12. Open the ***run.py*** and run CloudAlbum application with DynamoDB. ***(LAB03/01-DDB/run.py)***

* **NOTE:** **GMAPS_KEY** variable is must defined before you run.

* Ensure **Runner: Python 3**
<img src=./images/lab03-task1-run-console.png width=700>


13. Connect to your application using **Cloud9 preview** in your browser. 
<img src=images/lab01-08.png width=500>

* You need to **Sign-up** first.

14. Perform application test.
<img src=./images/lab01-02.png width=800>

* Sign in / up
* Upload Sample Photos
* Sample images download here
  *  https://d2r3btx883i63b.cloudfront.net/temp/sample-photo.zip
* Look your Album
* Change Profile
* Find photos with Search tool
* Check the Photo Map

15. Then look into AWS DynamoDB console.
* User and Photo tables are auto generated with 'user-email-index'
* Review saved data of each DynamoDB tables.
<img src=./images/lab03-task1-ddb_result.png width=800>

Is it OK? Let's move to the next TASK.

**NOTE:** Click the ***stop icon*** to stop your application.
  * **Close your terminal** after application stop.
  * **Close all your opened file tab.**
<img src=./images/stop-app.png width=500>

16. Delete data in the application for the next TASK.
* File system will be changed from **local disk** to **Amazon S3**.
* So, if you don't delete your album article which submitted this task, then **you will see your album article without images** when you run the application on the next TASK,

<img src=images/lab03-task2-delete.png width=400>


## TASK 3. Go to S3
CloudAlbum stored user uploaded images into disk based storage(EBS or NAS). However, disk storage has less scalability.

[Amazon S3](https://aws.amazon.com/s3/) has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites. The service aims to maximize benefits of scale and to pass those benefits on to developers.

<img src=./images/lab03-task2-arc.png width=600>

* We will use Boto3 - S3 API to handle uploaded photo image object from the user.
   * visit: https://boto3.readthedocs.io/en/latest/reference/services/s3.html

* We will retrieve image object with pre-signed URL and return it to the requested frontend side.

17. Make a bucket to save image objects and retrieve it from Amazon S3. Before copy and paste under below AWS cli command which create a S3 bucket, you should replace **cloudalbum-\<INITIAL\>** with your own initial to make a globally unique bucket name(e.g. cloudalbum-mrjb). We will use this bucket until end of this hands-on, please copy and paste your bucket name into your notes pad.

```
aws s3 mb s3://cloudalbum-<INITIAL>
```

18. Review the config.py file which located in *** LAB03/02-S3/backend/cloudalbum/config.py***

* Set up the value of 'S3_PHOTO_BUCKET'. Please change the **cloudalbum-\<INITIAL\>** to your **real bucket name** which made above.

```python
import datetime
import os

class BaseConfig:
	(...)
   
    # S3
    S3_PHOTO_BUCKET = os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-<your-initial>')
    S3_PRESIGNED_URL_EXPIRE_TIME = os.getenv('S3_PRESIGNED_URL_EXPIRE_TIME', 3600)
```

* As you can see, expire time for the presigned url of an object set 3600 seconds.


### TODO #5

19. Find **TODO #5** in the 'LAB03/02-S3/backend/cloudalbum/util/file_control.py' file and please implement your own code instead of following solution function which name is **solution\_put\_object\_to\_s3** to put an image object with Boto3 SDK. 

```python
	# TODO 5 : Implement following solution code to save image object to S3
	solution_put_object_to_s3(s3_client, key, original_bytes)
```

* Inside of the  **solution\_put\_object\_to\_s3**, you can find how to use Boto3 client to put an object into S3 bucket.

```python
	s3_client = boto3.client('s3')
	s3_client.put_object(
            Bucket=app.config['S3_PHOTO_BUCKET'],
            Key=key,
            Body=upload_file_stream,
            ContentType='image/jpeg',
            StorageClass='STANDARD'
        )
```


### TODO #6

20. Find **TODO #6** in the 'LAB03/02-S3/backend/cloudalbum/util/file_control.py' file and please implement your own code instead of following solution function which name is **solution\_generate\_s3\_presigned\_url** to generate an presigned url of each object. 

```python
    # TODO 6 : Implement following solution code to retrieve pre-signed URL from S3.
    url = solution_generate_s3_presigned_url(s3_client, key)
```
* Default expire time is 1 hour (3600 sec), we just defined expire time with same value in convinience. This is limited to under 36 hours. Below is Function description links.
	* Related document : https://boto3.readthedocs.io/en/latest/reference/services/s3.html 

```txt 
generate_presigned_url(ClientMethod, Params=None, ExpiresIn=3600, HttpMethod=None)

    Generate a presigned url given a client, its method, and arguments

    Parameters

            ClientMethod (string) -- The client method to presign for
            Params (dict) -- The parameters normally passed to ClientMethod.
            ExpiresIn (int) -- The number of seconds the presigned url is valid for. By default it expires in an hour (3600 seconds)
            HttpMethod (string) -- The http method to use on the generated url. By default, the http method is whatever is used in the method's model.

    Returns

        The presigned url
```


21. Open the ***run.py*** and run the application with DynamoDB and S3.

* Ensure **Runner: Python 3**
<img src=./images/lab03-task1-run-console.png width=800>

22. Connect to your application using **Cloud9 preview** in your browser. 

23. Perform application test.
<img src=./images/lab01-02.png width=700>

* Sign in / up
* Upload Sample Photos
* Sample images download here
  *  https://d2r3btx883i63b.cloudfront.net/temp/sample-photo.zip
* Look your Album
* Change Profile
* Find photos with Search tool
* Check the Photo Map

24. Examine DynamoDB Console and S3 Console.
<img src=./images/lab03-task2-s3-console.png width=500>

* You can find your uploaded image objects with thumbnails.

Is it OK? Let's move to the next TASK.

**NOTE:** Click the ***stop icon*** to stop your application.
  * **Close your terminal** after application stop.
  * **Close all your opened file tab.**
<img src=./images/stop-app.png width=500>


## TASK 4. Go to Cognito
In this TASK, you will add a sign-up/sign-in component to CloudAlbum application by using Amazon Cognito. After setting up Amazon Cognito user pool, user information will stored into the Amazon Cognito.

<img src=./images/lab03-task3-cognito-arc.png width=600>

To begin, follow the steps below.

**Set up an Amazon Cognito user pool.**

25. In the AWS Console, go to the **Amazon Cognito**

26. Make sure you are still in the **Singapore(ap-southeast-1)** region.

27. Click **Manage your User Pools**.

28. At the top right corner, click **Create a user pool**.

29. For **Pool name**, type **cloudalbum-pool-\<INITIAL\>**.

30. Click **Step through settings**.

31. For **How do you want your end users to sign in?**, select **Email address or phone number**.
<img src=./images/lab03-task3-cognito-setup.png width=800>

32. For **Which standard attributes do you want to require?**, select **name**.

33. Click **Next step**.

34. Leave the default settings on the Policy page and click **Next step**.

35. Skip the MFA and verifications pages and click **Next step**.

36. On the **Message customization** page, select **Verification Type** as **Link**. Feel free to customize the email body.

37. Click **Next Step**.

38. Skip the Tag section and click **Next Step**.

39. Leave the default setting on the **Devices** page and click **Next step**.

40. On the **App Clients** page, click **Add an app client**.

41. For **App client name,** type a client name, for example, **CloudAlbum**.

42. Leave the other default settings and click **Create app client**.

43. Click **Next Step**.

44. Skip the **Triggers** page and click **Next Step**

45. On the **Review** page, click **Create Pool**.

46. After the pool is created, write down the **Pool ID** for later use.

47. In the left navigation menu, under **App integration**, click **App client settings**.

48. For **Enabled Identity Providers**, check **Cognito User Pool**.
* Check the Cloud9 ResourceId at the **Cloud9 Terminal.** 
```console 
RESOURCE_ID=$(aws ec2 describe-tags --query "Tags[].Value" --filters "Name=resource-id, Values=`ec2-metadata --instance-id | cut -f2 -d ' '`" "Name=key, Values=aws:cloud9:environment" --output text)

echo "https://$RESOURCE_ID.vfs.cloud9.ap-southeast-1.amazonaws.com"

```
* **\<YOUR PREVIEW URL\>** is :  
```
https://<CLOUD9_RESOURCE_ID>.vfs.cloud9.ap-southeast-1.amazonaws.com
```
* **KEEP THIS VALUE FOR LATER USE**

 * For **Cloud9 Preview** user:
   * For **Callback URL(s)** type `https://<YOUR PREVIEW URL>/callback`
   * For **Sign out URL(s)** type `https://<YOUR PREVIEW URL>`
   * **NOTE:** This is an **alternative way** of check ResourceId. If you complete checking <YOUR PREVIEW URL>, You can pass below steps and go to STEP 49. 
   
   <img src='images/lab03-task3-cloud9-preview.png' width='550'>


49. Under **OAuth 2.0**, for **Allowed OAuth Flows**, select **Authorization code grant** and for **Allowed OAuth Scopes**, select **openid**.
<img src="images/lab03-task2-cognito-app-client.png" width="500">

50. Click **Save changes** at the bottom.

51. In the left navigation menu, under **App integration**, click **Domain name**.

52. Type a **domain name**(for example: `cloudalbum-<INITIAL>`, check its availability, and click **Save changes**. Write down the domain name for later use.
 * **NOTE:** Domain name You have to use **lowercase**.
<img src="images/lab03-task2-cognito-domain.png" width="500">

53. In the left navigation menu, under **General settings**, click **App clients**.

54. Click **Show details**.

55. Make a note of the **App client ID** and **App client secret** for later use.

56. Click **Return to pool details** at the bottom to return to the Pool details page.


57. Install required Python packages:
```console
sudo pip-3.6 install -r ~/environment/moving-to-serverless-workshop-1d/LAB03/03-CloudAlbum-COGNITO/requirements.txt
```

58. Review 'LAB03/03-COGNITO/cloudalbum/config.py'

* Set up **S3_PHOTO_BUCKET** value : Replace **cloudalbum-\<INITIAL\>** to exist value which created previous hands-on lab.

```python
import datetime
import os

class BaseConfig:
	(...)
	# S3
	S3_PHOTO_BUCKET = os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-<your-initial>')
	
	# COGNITO
	'COGNITO_POOL_ID' = os.getenv('COGNITO_POOL_ID', '<YOUR_POOL_ID>')
	'COGNITO_CLIENT_ID' = os.getenv('COGNITO_CLIENT_ID', '<YOUR_CLIENT_ID>')
	'COGNITO_CLIENT_SECRET' = os.getenv('COGNITO_CLIENT_SECRET', '<YOUR_CLIENT_SECRET>')
	'COGNITO_DOMAIN' = os.getenv('COGNITO_DOMAIN', '<YOUR_COGNITO_DOMAIN>')

```

* Check the values under ***# COGNITO***.
* The second parameter of **os.getenv** is the default value to use when the first parameter does not exist.

| COGNITO_POOL_ID | Copy and paste the pool ID you noted earlier. |
----|----
| COGNITO_CLIENT_ID | Copy and paste the App Client ID you noted earlier. |
| COGNITO_CLIENT_SECRET | Copy and paste the App Client Secret you noted earlier. |
|COGNITO_DOMAIN |Copy and paste the domain name you created earlier. It should look similar to the example below. Do not copy the entire URL starting with https://<YOUR_DOMAIN_NAME>.auth.ap-southeast-1.amazoncognito.com (for example(**without** `https://`): <YOUR_DOMAIN_NAME>.auth.ap-southeast-1.amazoncognito.com)|

 * For example,

   <img src="images/lab03-task3-cognito-config.png" width="800">



### TODO #7
59. Find **TODO #7** in the 'LAB03/03-Cognito/backend/cloudalbum/api/users.py' file and please implement your own code instead of following solution function which name is **solution\_signup\_cognito** which is enroll user into Cognito user pool.

```python
	# TODO 7: Implement following solution code to sign up user into cognito user pool
	return solution_signup_cognito(user, dig)
```

* Inside of the function, you can find how to create a user into Cognito user pool with Boto3. Let's review the code.

```python
	client = boto3.client('cognito-idp')
	
	response = client.sign_up(
            ClientId=app.config['COGNITO_CLIENT_ID'],
            SecretHash=base64.b64encode(dig).decode(),
            Username=user['email'],
            Password=user['password'],
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': user['username']
                }
            ],
            ValidationData=[
                {
                    'Name': 'name',
                    'Value': user['username']
                }
            ]

        )
```

* UserAttributes means attributes that you checked when create Cognito user pool. According to upper code, your new user's attributes which stored in Cognito will look like this. This data structure is different from Cloudalbum's key name. 


```json
{
	"username": "user_email@a.c",
	"password": "password",
	"name": "user_name of CloudAlbum"
}
```

* For instance, in CloudAlbum, the key name of email was just 'email', however it need to be changed into 'username' when stored into Cognito. 

* After register a user into Cognito User pool, admin need to confirm that user. For your convinience, We automatically confirmed user right after success to register. Please refer below code which is located in **LAB03/03-Cognito/backend/cloudalbum/soultion.py**

```python 
def user_signup_confirm(id):
    client = boto3.client('cognito-idp')
    try:
        client.admin_confirm_sign_up(
            UserPoolId=conf['COGNITO_POOL_ID'],
            Username=id
        )
        app.logger.debug('success: user confirm automatically:user id:{}'.format(id))
    except Exception as e:
        app.logger.error('ERROR: user confirm failed:user id:{}'.format(id))
        app.logger.error(e)
```

### TODO #8

60. Find **TODO #8** in the **LAB03/03-Cognito/backend/cloudalbum/api/users.py** file and please implement your own code instead of following solution function which name is **solution\_get\_cognito\_user\_data**. This function get user data from Cognito user pool with access_token with Boto3. 

```python
	# TODO 8: Implement follwing solution code to get user data from Cognito user pool
	return solution_get_cognito_user_data(access_token)
```

* Let's look around **solution\_get\_cognito\_user\_data** function. All you need to implement is making a call to Boto3 get_user function, and parsing the the response to set it properly as CloudAlbum's key name.

```python
	cognito_user = client.get_user(AccessToken=access_token)
	
	user_data = {}
	for attr in cognito_user['UserAttributes']:
	    key = attr['Name']
	    if key == 'sub':
	        key = 'user_id'
	    val = attr['Value']
	    user_data[key] = val
```


61. **Open the run.py** and run the application. Connect to your application using **Cloud9 preview**in your browser. 
* You can find default Cognito Login Screen.
<img src="images/lab03-task3-cognito-login.png" width="450">

* You need to verify your email address after signup.
<img src="images/lab03-task3-cog-verify.png" width="450">

* You can **change default login screen** in the Cognito console dashboard.


62. Perform application test.
<img src=./images/lab01-02.png width=500>

* Sign in / up
* Upload Sample Photos
* Sample images download here
  *  https://d2r3btx883i63b.cloudfront.net/temp/sample-photo.zip
* Look your Album
* Change Profile
* Find photos with Search tool
* Check the Photo Map

63. Examine Cognito Console dashboard **after user sign-up.**
<img src=./images/lab03-task3-cognito-userpool.png width=700>

* You can find your profile information.

Is it OK? Let's move to the next TASK.

**NOTE:** Click the ***stop icon*** to stop your application.
  * **Close your terminal** after application stop.
  * **Close all your opened file tab.**
<img src=./images/stop-app.png width=500>

## TASK 5. Go to X-ray

AWS [X-Ray](https://aws.amazon.com/xray/) helps developers analyze and debug production, distributed applications, such as those built using a microservices architecture. With X-Ray, you can understand how your application and its underlying services are performing to identify and troubleshoot the root cause of performance issues and errors. X-Ray provides an end-to-end view of requests as they travel through your application, and shows a map of your application’s underlying components. You can use X-Ray to analyze both applications in development and in production, from simple three-tier applications to complex microservices applications consisting of thousands of services.

<img src="./images/lab03-task4-x-ray-arc.png" width="600">

64. Install required Python packages for AWS X-Ray.
```console
sudo pip-3.6 install -r ~/environment/moving-to-serverless-workshop-1d/LAB03/04-CloudAlbum-XRAY/requirements.txt
```

**Download and run the AWS X-Ray daemon on your AWS Cloud9 instance.**

65. Visit the AWS X-Ray daemon documentation link below:
* https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html

66. On the documentation page, scroll down until you see a link to **Linux (executable)-aws-xray-daemon-linux-2.x.zip (sig).** Right-click the link and copy the link address.

67. In your AWS **Cloud9 instance terminal**, type the command below to go to your home directory.
```console
cd ~
```

68. Type wget and paste the AWS X-Ray daemon hyperlink address that you copied. The command should look like the example below.
```console
wget https://s3.dualstack.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-3.x.zip
```

69. Unzip the AWS X-Ray daemon by typing the command below. Make sure that the name of the .zip file matches the one in the command below.
```console
unzip aws-xray-daemon-linux-3.x.zip
```

70. Run the AWS X-Ray daemon by typing the command below. The X-Ray daemon buffers segments in a queue and uploads them to X-Ray in batches. 

```console
./xray
```

* **Now, X-Ray daemon works and ready to use X-Ray to analyze applications.**

### TODO #9

70. Review TODO #9 which is in **LAB03/04-XRAY/cloudalbum/backend/__init__.py** file.

* To instrument CloudAlbum, *our Flask application*, first configure a segment name on the xray_recorder. Then, use the XRayMiddleware function to patch our CloudAlbum application in code. 
* Related document
   * https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-configuration.html
   * https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-middleware.html


```python
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

(...)
	
	# TODO 9: Review X-ray setting
	patch_modules = (
	    'boto3',
	    'botocore',
	    'pynamodb',
	    'requests',
	)
	plugins = ('EC2Plugin',)
	xray_recorder.configure(service='CloudAlbum',
	                        plugins=plugins,
	                        context_missing='LOG_ERROR',
	                        sampling=False)
	
	XRayMiddleware(app, xray_recorder)
	patch(patch_modules)
    
(...)
```

* To instrument downstream calls, define libraries that your application uses into patch_modules. The X-Ray SDK for Python can patch the following libraries.
	* **NOTE:** Patching Libraries to Instrument Downstream Calls
	* https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-patching.html

* Sampling keywords argument tells the X-Ray recorder to trace requests served by your Flask application with the default sampling rate. You can configure the recorder in code to apply custom sampling rules or change other settings. 

**NOTE**: You can use 'xray_recorder' decorator to capture function execution information.

```python
from aws_xray_sdk.core import xray_recorder
(...)

@xray_recorder.capture()
def print_abc():
    print('abc')

```


71. Implement your unique data into **LAB03/04-XRAY/cloudalbum/backend/config.py**. This step is identical to the step 58.

* Set up **S3_PHOTO_BUCKET** value : Replace **cloudalbum-\<INITIAL\>** to real value which used previous hands-on lab.

```
import datetime
import os

class BaseConfig:
	(...)
	# S3
	S3_PHOTO_BUCKET = os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-<your-initial>')
		
	# COGNITO
	'COGNITO_POOL_ID' = os.getenv('COGNITO_POOL_ID', '<YOUR_POOL_ID>')
	'COGNITO_CLIENT_ID' = os.getenv('COGNITO_CLIENT_ID', '<YOUR_CLIENT_ID>')
	'COGNITO_CLIENT_SECRET' = os.getenv('COGNITO_CLIENT_SECRET', '<YOUR_CLIENT_SECRET>')
	'COGNITO_DOMAIN' = os.getenv('COGNITO_DOMAIN', '<YOUR_COGNITO_DOMAIN>')
```

* Check the values under ***# COGNITO***.
* The second parameter of **os.getenv** is the default value to use when the first parameter does not exist.

| COGNITO_POOL_ID | Copy and paste the pool ID you noted earlier. |
----|----
| COGNITO_CLIENT_ID | Copy and paste the App Client ID you noted earlier. |
| COGNITO_CLIENT_SECRET | Copy and paste the App Client Secret you noted earlier. |
|COGNITO_DOMAIN |Copy and paste the domain name you created earlier. It should look similar to the example below. Do not copy the entire URL starting with https://<YOUR_DOMAIN_NAME>.auth.ap-southeast-1.amazoncognito.com (for example(**without** `https://`): <YOUR_DOMAIN_NAME>.auth.ap-southeast-1.amazoncognito.com)|

 * For example,

   <img src="images/lab03-task3-cognito-config.png" width="800">

72. **Open the run.py** and run the application. You can run the application to check all features are works well. Then you will see function tracing data collected on the X-Ray console.

73. Connect to your application using **Cloud9 preview** in your browser. 
* You can find default Cognito Login Screen.
<img src=images/lab03-task3-cognito-login.png width=500>

* You can change default login screen in the Cognito console dashboard.

74. Perform application test.

<img src=images/lab01-02.png width=700>

* Sign in / up
* Upload Sample Photos
* Sample images download here
  *  https://d2r3btx883i63b.cloudfront.net/temp/sample-photo.zip
* Look your Album
* Change Profile
* Find photos with Search tool
* Check the Photo Map

75. Examine X-Ray Console dashboard
<img src=images/lab03-task4-x-ray.png width=500>

Is it OK? Let's go to next LAB.

**NOTE:** Click the ***stop icon*** to stop your application.
  * **Close your terminal** after application stop.
  * **Close all your opened file tab.**
<img src=images/stop-app.png width=700>


# Congratulation! You completed LAB03.

## LAB GUIDE LINKS
* [LAB 01 - Take a look around](LAB01.md)
* [LAB 02 - Building and deploying your application in HA environment](LAB02.md)
* [LAB 03 - Move to serverless](LAB03.md)
* [LAB 04 - Serverless with AWS Chalice](LAB04.md)
