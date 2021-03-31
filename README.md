# Moving to AWS Serverless.
<img src="lab-guide/images/Serverless-logo-github.png" width=640>




## Welcome! ##
This workshop content will handle the server based Python Flask web application and show how to move to Serverless architecture application using AWS Chalice micro-framework. It deals with how to rewrite application source code from a server-based application into a serverless environment step by step with practical application level. This workshop cover Cloud9, S3, API Gateway, Lambda, Cognito, DynamoDB, X-Ray, Parameter Store with AWS Chalice micro-framework. This workshop contains four short presentations and four hands-on labs. The application used in the hands-on labs consists of an SPA frontend based on vue.js and a RESTFul backend based on Flask. Application source code and hands-on lab guides are providing via Github repository.

#### Written by
 * Sungshik Jou (AWS Technical Trainer)
 * Dayoungle Jun (AWS Technical Trainer)
 * YoungSeon.Ahn (https://github.com/LoveMeWithoutAll)

#### Improvements
 * Sample applications have been redesigned to a better architecture.
 * with Vue.js based SPA frontend.
 * with Flask based restful backend.
 * with Swagger support.
 * with token based authentication.
 * Eliminate user inconvenience on Hands on-lab.
 * Remove Google MAP API dependencies with Leaflet.


##### Previous Version
* 2019.03 ~ 2019.05 : https://github.com/aws-kr-tnc/moving-to-serverless-workshop-1d
  * Four hands-on lab, full day. (4 slidedeck)
* 2018.11 : https://github.com/aws-kr-tnc/moving-to-serverless-techpump
  * Three hands-on labs, half day. (4 slidedeck)
* 2018.08 : https://github.com/liks79/aws-chalice-migration-workshop
  * Three hands-on labs, half day. (3 slidedeck)
 


## Hands-on LAB GUIDES
* [Lab 1: CloudAlbum with 3-tier Architecture](lab-guide/LAB01.md)
	* [TASK 1. Create AWS Cloud9 environment and explore the environment](lab-guide/LAB01.md#task-1-create-aws-cloud9-environment-and-explore-the-environment)
	* [TASK 2. Look around legacy application and try run it](lab-guide/LAB01.md#task-2-look-around-legacy-application-and-try-run-it)
	* [TASK 3. Connect to your application (Cloud9)](lab-guide/LAB01.md#task-3-optional-task-connect-to-your-application-ssh-tunneling)
	* [TASK 4. Take a look around](lab-guide/LAB01.md#task-4-take-a-look-around)
	* [TASK 5. Stop your application](lab-guide/LAB01.md#task-5-stop-your-application)
	
* [Lab 2: CloudAlbum with 3-tier architecture and high availability](lab-guide/LAB02.md)
	* [TASK 1. Create your multi-az VPC](lab-guide/LAB02.md#task-1-create-your-multi-az-vpc)
	* [TASK 2. Create EFS](lab-guide/LAB02.md#task-2-create-efs)
	* [TASK 3. Create Elasticache](lab-guide/LAB02.md#task-3-create-elasticache)
	* [TASK 4. Confiugure ElasticBeanstalk](lab-guide/LAB02.md#task-4-confiugure-elasticbeanstalk)
	* [TASK 5. Deploy Application with ElasticBeanstalk](lab-guide/LAB02.md#task-5-deploy-application-with-elasticbeanstalk)
	* [TASK 6. Perform application test](lab-guide/LAB02.md#task-6-perform-application-test)
	* [TASK 7. Remove your AWS resources](lab-guide/LAB02.md#task-7-remove-your-aws-resources)

* [Lab 3: CloudAlbum with Serverless Architecture - Part 1](lab-guide/LAB03.md)
	* [TASK 1. Permission grant for Cloud9](lab-guide/LAB03.md#task-0-permission-grant-for-cloud9)
	* [TASK 2. Go to DynamoDB](lab-guide/LAB03.md#task-1-go-to-dynamodb)
	* [TASK 3. Go to S3](lab-guide/LAB03.md#task-2-go-to-s3)
	* [TASK 4. Go to Cognito](lab-guide/LAB03.md#task-2-go-to-s3)
	* [TASK 5. Go to X-ray](lab-guide/LAB03.md#task-2-go-to-s3)

* [Lab 4: CloudAlbum with Serverless Architecture - Part 2](lab-guide/LAB04.md)
	* [TASK 1. Setup virtualenv](lab-guide/LAB04.md#task-1--seyup-virtualenv)
	* [TASK 2. Build a simple AWS Chalice serverless app](lab-guide/LAB04.md#task-2--build-a-simple-aws-chalice-serverless-app)
	* [TASK 3. CloudAlbum with AWS Chalice](lab-guide/LAB04.md#task-3--cloudalbum-with-aws-chalice)


