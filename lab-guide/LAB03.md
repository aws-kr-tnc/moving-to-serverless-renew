# Lab 3: CloudAlbum with Serverless Architecture - Part 1
Now, we will move the components of legacy application which has constraints of scalability and high availability to serverless environment one by one.

**NOTE:** You can download all source code related this lab like below.
```console
cd ~/environment
wget https://raw.githubusercontent.com/aws-kr-tnc/moving-to-serverless-renew/master/resources/cloudalbum-mts-dist-src.zip
unzip cloudalbum-mts-dist-src.zip
mv cloudalbum-mts-dist-src/* .
rm -R cloudalbum-mts-dist-src
rm cloudalbum-mts-dist-src.zip
```

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

* **For CLI (local machine or EC2) users** : [CLI GUIDE (click)](LAB03-ROLE-CLI.md)

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
* Ok. You made the IAM policy for the role.
* Next, you will make "assume role" with the predefined policy.
* Click **Role** on the left menu.
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

* We already made `venv` and activated.

```console
pip install -r ~/environment/LAB03/01-DDB/backend/requirements.txt
```



2. Review the data model definition via **SQLAlchemy**. **User** table and **Photo** table are inherited from SQLAlchemy's **db.Model** and are represented in **Python classes**.

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

* SQLAlchemy is a very popular Data Mapper in the Python world. It is simplifying database workflows, providing an ORM, and integrating into other major Python libraries.

2. Open the **models_ddb.py** which located in  **LAB03/01-DDB/backend/cloudalbum/database/models_ddb.py**.
<img src=./images/lab03-task1-models_ddb-2.png width=300>



3. Review the data model definition via **PynamoDB**. This will show how DynamoDB tables and GSI are defined in PynamoDB. They are all expressed in **Python Class.**

```python
import json
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, ListAttribute, MapAttribute
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection
from tzlocal import get_localzone
from boto3.session import Session
from os import environ


AWS_REGION = Session().region_name if environ.get('AWS_REGION') is None else environ.get('AWS_REGION')


class EmailIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = 'user-email-index'
        read_capacity_units = 5
        write_capacity_units = 5
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
        region = AWS_REGION

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
        region = AWS_REGION

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

...
```

6. Review the **__init__.py** in the database package. The DynamoDB **User** and **Photo** tables will be **created automatically** for the convenience. **Note** the **(Model).create_table** function which used in **LAB03/01-DDB/backend/cloudalbum/database/__init__.py**. This is a feature of Pynamodb Model class.

```python
from cloudalbum.database.model_ddb import User, Photo
from flask import current_app as app


def create_table():
    if not User.exists():
        app.logger.debug('Creating DynamoDB User table..')
        User.create_table(read_capacity_units=app.config['DDB_RCU'],
                          write_capacity_units=app.config['DDB_WCU'],
                          wait=True)
    if not Photo.exists():
        app.logger.debug('Creating DynamoDB Photo table..')
        Photo.create_table(read_capacity_units=app.config['DDB_RCU'],
                           write_capacity_units=app.config['DDB_WCU'],
                           wait=True)


def delete_table():
    if User.exists():
        User.delete_table()
    if Photo.exists():
        Photo.delete_table()
```

7. Review the **LAB03/01-DDB/backend/cloudalbum/config.py** file. **New attributes** are added for DynamoDB.

* The second parameter of **os.getenv** function is the default value to use when the first parameter does not exist.

```python
import os
import datetime
from os import environ
from boto3.session import Session

class BaseConfig:
	(.. ..)
	
    AWS_REGION = Session().region_name if environ.get('AWS_REGION') is None else environ.get('AWS_REGION')

    # DynamoDB
    DDB_RCU = int(os.getenv('DDB_RCU', '10'))
    DDB_WCU = int(os.getenv('DDB_WCU', '10'))


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
        raise BadRequest('Not existed user!')
    else:
        ....

```
* Above solution code shows the way of using GSI which has a partition key as email.

* Inside of **solution\_get\_user\_data\_with\_idx** function, you can find how to query to GSI **email_index**, which is defined at LAB03/01-DDB/backend/cloudalbum/database/model_ddb.py.

```python
    user_email = [item for item in User.email_index.query(signin_data['email'])]
    if not user_email:
        return None
    return user_email[0]

```


### TODO #3

10. Find **TODO #3** in the **LAB03/01-DDB/backend/cloudalbum/api/photos.py** file and please implement your own code instead of following solution function which name is **solution\_put\_photo\_info\_ddb** to put item into Photo table.

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

11. Find **TODO #4** in the **LAB03/01-DDB/backend/cloudalbum/api/photos.py** file and please implement your own code instead of following solution function which name is **solution\_delete\_photo\_from\_ddb** to delete item from Photo table.

```python
	# TODO 4: Implement following solution code to delete a photo from Photos which is a list
	filename = solution_delete_photo_from_ddb(user, photo_id)
```

12. Inside of **solution\_delete\_photo\_from\_ddb** function, you can find how to delete an item from Photo table with Pynamodb api.

```python
	photo = Photo.get(user['user_id'], photo_id)
	photo.delete()
```

**NOTE:** Now, we converted backend application source code to use DynamoDB, an Amazon serverless datastore, instead of the RDBMS. Amazon DynamoDB is a fully managed serverless datastore. We no longer need to take the scalability and server management burden off.


13. Now we can run unittest to check if our application is working properly. 

* Before, run unittest you need to load environment variables for the application. You can check this `~/environment/LAB03/01-DDB/backend/shell.env` file.

* You can also check `~/environment/LAB03/01-DDB/backend/cloudalbum/config.py` file. Each default value of `DDB_RCU` and `DDB_WCU` is 10.


```console
source ~/environment/LAB03/01-DDB/backend/shell.env
cd ~/environment/LAB03/01-DDB/backend/cloudalbum/tests
```
* Run pytest like below.
```console
pytest -v -W ignore::DeprecationWarning
```
* Output
```console
================================ test session starts ================================
platform linux -- Python 3.6.8, pytest-5.1.2, py-1.8.0, pluggy-0.13.0 -- /home/ec2-user/environment/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/ec2-user/environment/LAB03/01-DDB/backend/cloudalbum/tests
plugins: cov-2.7.1
collected 25 items                                                                  

test_admin.py::TestAdminService::test_healthcheck PASSED                      [  4%]
test_admin.py::TestAdminService::test_ping PASSED                             [  8%]
test_config.py::TestDevelopmentConfig::test_app_is_development PASSED         [ 12%]
test_config.py::TestDevelopmentConfig::test_ddb_rcu PASSED                    [ 16%]
test_config.py::TestDevelopmentConfig::test_ddb_wcu PASSED                    [ 20%]
test_config.py::TestTestingConfig::test_app_is_testing PASSED                 [ 24%]
test_config.py::TestTestingConfig::test_ddb_rcu PASSED                        [ 28%]
test_config.py::TestTestingConfig::test_ddb_wcu PASSED                        [ 32%]
test_config.py::TestProductionConfig::test_app_is_production PASSED           [ 36%]
test_config.py::TestProductionConfig::test_ddb_rcu PASSED                     [ 40%]
test_config.py::TestProductionConfig::test_ddb_wcu PASSED                     [ 44%]
test_dynamodb.py::TestDynamoDBService::test_photo_table PASSED                [ 48%]
test_dynamodb.py::TestDynamoDBService::test_user_table PASSED                 [ 52%]
test_photos.py::TestPhotoService::test_delete PASSED                          [ 56%]
test_photos.py::TestPhotoService::test_get_mode_thumb_orig PASSED             [ 60%]
test_photos.py::TestPhotoService::test_list PASSED                            [ 64%]
test_photos.py::TestPhotoService::test_ping PASSED                            [ 68%]
test_photos.py::TestPhotoService::test_upload PASSED                          [ 72%]
test_users.py::TestUserService::test_bad_signin PASSED                        [ 76%]
test_users.py::TestUserService::test_bad_signup PASSED                        [ 80%]
test_users.py::TestUserService::test_ping PASSED                              [ 84%]
test_users.py::TestUserService::test_signin PASSED                            [ 88%]
test_users.py::TestUserService::test_signout PASSED                           [ 92%]
test_users.py::TestUserService::test_signup PASSED                            [ 96%]
test_users.py::TestUserService::test_signup_duplicate_email PASSED            [100%]
================================ 25 passed in 3.31s =================================
```

* If the test fails, you can check the environment variables in the `~/environment/LAB03/01-DDB/backend/shell.env` file. Nevertheless, if you cannot solve the problem, contact the instructor.

14. Now, you can run CloudAlbum application like below after unittest. Let's run backend and frontend.
* for backend
```console
cd ~/environment/LAB03/01-DDB/backend
python manage.py run -h 0.0.0.0 -p 5000 
```
* for frontend (use another terminal in Cloud9)
```console
cd ~/environment/frontend/cloudalbum
npm run serve
```

  * You can also refer to following lab guide in LAB01.
    * [TASK 3. Connect to your application (Via SSH Tunneling)](LAB01.md#task-3-connect-to-your-application-(via-ssh-tunneling)) 
    * [TASK 2. Look around current application and try run it.](LAB01.md#task-2.-look-around-current-application-and-try-run-it.)

15. Enjoy the CloudAlbum with DynamoDB
  * You can use `python manage.py seed_db` command to create test user easily.

<img src=./images/lab01-02.png width=700>


16. Then look into AWS DynamoDB console.
* User and Photo tables are generated automatically with 'user-email-index'
* Review saved data of each DynamoDB tables.
<img src=./images/lab03-task1-ddb_result.png width=800>

Is it OK? Let's move to the next TASK.

17. If you are running a backend or frontend application, you can exit by pressing `ctrl + c`.


## TASK 3. Go to S3
CloudAlbum stored user uploaded images into disk based storage(EBS or NAS). However, disk storage has less scalability.

[Amazon S3](https://aws.amazon.com/s3/) has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites. The service aims to maximize benefits of scale and to pass those benefits on to developers.

<img src=./images/lab03-task2-arc.png width=600>

* We will use Boto3 - S3 API to handle uploaded photo image object from the user.
   * visit: https://boto3.readthedocs.io/en/latest/reference/services/s3.html

* We will retrieve image object with pre-signed URL and return it to the requested frontend side.
* For your convenience, let's set frontend variable ```VUE_APP_S3_PRESIGNED_URL``` value to **true**. You can find this variable in **~/environment/frontend/cloudalbum/.env**.

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

18. Now, let's build front-end application for handle S3 presigned URL.

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

19. We have already made an S3 Bucket for the frontend at LAB02. If you haven't created an S3 bucket on LAB01, you can create it like this. We use this bucket to save image objects and retrieve it.

* Before copy and paste under below AWS cli command which create a S3 bucket, you should replace **cloudalbum-\<INITIAL\>** with your own initial to make a globally unique bucket name(e.g. cloudalbum-mrjb). 


```console
aws s3 mb s3://cloudalbum-<your-initial>
```

* You can see the message like below
```console
make_bucket: cloudalbum-<your-initial>
```

**Now, we will change our source code to save uploaded photo files to S3.**


20. Let's review the config.py file which located in **LAB03/02-S3/backend/cloudalbum/config.py**

```python
import os
import datetime
from os import environ
from boto3.session import Session


class BaseConfig:
...
   
    # S3
    S3_PHOTO_BUCKET = os.getenv('S3_PHOTO_BUCKET', None)
    S3_PRESIGNED_URL_EXPIRE_TIME = int(os.getenv('S3_PRESIGNED_URL_EXPIRE_TIME', '3600'))
...
```

21. You can set up the value of 'S3_PHOTO_BUCKET'  in `~/environment/LAB03/02-S3/backend/shell.env` file. 
```bash
# Required environment variables
export UPLOAD_FOLDER=/tmp
export FLASK_APP=cloudalbum/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=cloudalbum.config.DevelopmentConfig
export DDB_RCU=10
export DDB_WCU=10
export S3_PHOTO_BUCKET=
export S3_PRESIGNED_URL_EXPIRE_TIME=3600
# export COGNITO_POOL_ID=
# export COGNITO_CLIENT_ID=
# export COGNITO_CLIENT_SECRET=

```
* Uncomment `# export S3_PHOTO_BUCKET=` and assign your own bucket name.


* As you can see, expire time for the presigned url of an object set 3600 seconds.


### TODO #5

22. Find **TODO #5** in the 'LAB03/02-S3/backend/cloudalbum/util/file_control.py' file and please implement your own code instead of following solution function which name is **solution\_put\_object\_to\_s3** to put an image object with Boto3 SDK. 

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

23. Find **TODO #6** in the 'LAB03/02-S3/backend/cloudalbum/util/file_control.py' file and please implement your own code instead of following solution function which name is **solution\_generate\_s3\_presigned\_url** to generate an presigned url of each object. 

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
**NOTE:** Why we use **Presigned URL** instead of byte-stream as previous lab?
* **Someone who receives the presigned URL can access the object**. 
  * First, it helps **Single Page Application to fetch images without any auth token** which should be sent in ```Authorization``` header. Furthermore, images(or other static assets) behind authentication is quite difficult to implement. 
  * Second, presigned URL support your **server side application to off-load it's role to send a static data to browser**. It helps to distributed environment between client and server application. Once the browser get the image url, it can request image to the S3 by self without any server-side authentication.
	* visit: https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURL.html


24. Now we can run unittest to check if our application is working properly. 

* Before, run unittest you need to load environment variables for the application. You can check this `~/environment/LAB03/02-S3/backend/shell.env` file.

* You can also check `~/environment/LAB03/02-S3/backend/cloudalbum/config.py` file. Configure `S3_PHOTO_BUCKET` value and uncomment this. Before run `source shell.env`.

```console
# Required environment variables
export UPLOAD_FOLDER=/tmp
export FLASK_APP=cloudalbum/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=cloudalbum.config.DevelopmentConfig
export DDB_RCU=10
export DDB_WCU=10
export S3_PHOTO_BUCKET=
export S3_PRESIGNED_URL_EXPIRE_TIME=3600
# export COGNITO_POOL_ID=
# export COGNITO_CLIENT_ID=
# export COGNITO_CLIENT_SECRET=
```

```console
source ~/environment/LAB03/02-S3/backend/shell.env
cd ~/environment/LAB03/02-S3/backend/cloudalbum/tests
```
* Run unittest like below.
```console
pytest -v -W ignore::DeprecationWarning
```
* Output
```console
============================= test session starts =============================
platform linux -- Python 3.6.8, pytest-5.1.2, py-1.8.0, pluggy-0.13.0 -- /home/ec2-user/environment/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/ec2-user/environment/LAB03/02-S3/backend/cloudalbum/tests
plugins: cov-2.7.1
collected 29 items                                                            

test_admin.py::TestAdminService::test_healthcheck PASSED                [  3%]
test_admin.py::TestAdminService::test_ping PASSED                       [  6%]
test_config.py::TestDevelopmentConfig::test_app_is_development PASSED   [ 10%]
test_config.py::TestDevelopmentConfig::test_ddb_rcu PASSED              [ 13%]
test_config.py::TestDevelopmentConfig::test_ddb_wcu PASSED              [ 17%]
test_config.py::TestDevelopmentConfig::test_s3_bucket PASSED            [ 20%]
test_config.py::TestTestingConfig::test_app_is_testing PASSED           [ 24%]
test_config.py::TestTestingConfig::test_ddb_rcu PASSED                  [ 27%]
test_config.py::TestTestingConfig::test_ddb_wcu PASSED                  [ 31%]
test_config.py::TestTestingConfig::test_s3_bucket PASSED                [ 34%]
test_config.py::TestProductionConfig::test_app_is_production PASSED     [ 37%]
test_config.py::TestProductionConfig::test_ddb_rcu PASSED               [ 41%]
test_config.py::TestProductionConfig::test_ddb_wcu PASSED               [ 44%]
test_config.py::TestProductionConfig::test_s3_bucket PASSED             [ 48%]
test_dynamodb.py::TestDynamoDBService::test_photo_table PASSED          [ 51%]
test_dynamodb.py::TestDynamoDBService::test_user_table PASSED           [ 55%]
test_photos.py::TestPhotoService::test_delete PASSED                    [ 58%]
test_photos.py::TestPhotoService::test_get_mode_thumb_orig PASSED       [ 62%]
test_photos.py::TestPhotoService::test_list PASSED                      [ 65%]
test_photos.py::TestPhotoService::test_ping PASSED                      [ 68%]
test_photos.py::TestPhotoService::test_upload PASSED                    [ 72%]
test_s3.py::TestS3Service::test_bucket_availability PASSED              [ 75%]
test_users.py::TestUserService::test_bad_signin PASSED                  [ 79%]
test_users.py::TestUserService::test_bad_signup PASSED                  [ 82%]
test_users.py::TestUserService::test_ping PASSED                        [ 86%]
test_users.py::TestUserService::test_signin PASSED                      [ 89%]
test_users.py::TestUserService::test_signout PASSED                     [ 93%]
test_users.py::TestUserService::test_signup PASSED                      [ 96%]
test_users.py::TestUserService::test_signup_duplicate_email PASSED      [100%]
============================= 29 passed in 3.82s ==============================
```

24. You can run CloudAlbum application like below after unittest.
  * for backend.
```console
cd ~/environment/LAB03/02-S3/backend
python manage.py run -h 0.0.0.0 -p 5000 
```
  * for frontend. (use another terminal in Cloud9)
```console
cd ~/environment/frontend/cloudalbum/
npm run serve
```

  * You can also refer to 
  [TASK 3. Connect to your application (Via SSH Tunneling)](LAB01.md#task-3-connect-to-your-application-(via-ssh-tunneling)) and [TASK 2. Look around current application and try run it.](LAB01.md#task-2.-look-around-current-application-and-try-run-it.)in LAB01.

25. Enjoy the CloudAlbum with DynamoDB and S3
  * You can use `python manage.py seed_db` command to create test user easily.

<img src=./images/lab01-02.png width=700>


26. Examine DynamoDB Console and S3 Console.
<img src=./images/lab03-task2-s3-console.png width=500>

* You can find your uploaded image objects with thumbnails.

Is it OK? Let's move to the next TASK.

27. Stop your application. 
* You can stop both frontend and backend application by press `ctrl+c` in your Cloud9 Terminal.


## TASK 4. Go to Cognito
In this TASK, you will add a sign-up/sign-in component to CloudAlbum application by using Amazon Cognito. After setting up Amazon Cognito user pool, user information will stored into the Amazon Cognito.

<img src=./images/lab03-task3-cognito-arc.png width=600>

To begin, follow the steps below.

**Set up an Amazon Cognito user pool.**

28. In the AWS Console, go to the **Amazon Cognito**

29. Make sure you are still in the **Singapore(ap-southeast-1)** region.

30. Click **Manage your User Pools**.

31. At the top right corner, click **Create a user pool**.

32. For **Pool name**, type **cloudalbum-pool-\<INITIAL\>**.

33. Click **Step through settings**.

34. For **How do you want your end users to sign in?**, select **Email address or phone number**.
<img src=./images/lab03-task3-cognito-setup.png width=800>

35. For **Which standard attributes do you want to require?**, select **name**.

36. Click **Next step**.

37. Leave the default settings on the Policy page and click **Next step**.

38. Skip the MFA and verifications pages and click **Next step**.

39. On the **Message customization** page, select **Verification Type** as **Link**. Feel free to customize the email body.

40. Click **Next Step**.

41. Skip the Tag section and click **Next Step**.

42. Leave the default setting on the **Devices** page and click **Next step**.

43. On the **App Clients** page, click **Add an app client**.

44. For **App client name,** type a client name, for example, **CloudAlbum**.

45. Choose **Enable sign-in API for server-based authentication (ADMIN_NO_SRP_AUTH)** option.
<img src=./images/lab03-task3-cognito-app-client.png width=800>

46. Leave the other default settings and click **Create app client**.

47. Click **Next Step**.

48. Skip the **Triggers** page and click **Next Step**

49. On the **Review** page, click **Create Pool**.

50. After the pool is created, write down the **Pool ID** for later use.

51. In the left navigation menu, under **App integration**, click **App client settings**.

52. In the left navigation menu, under **General settings**, click **App clients**.

53. Click **Show details**.

54. Make a note of the **App client ID** and **App client secret** for later use.

55. Click **Return to pool details** at the bottom to return to the Pool details page.


56. Install required Python packages:
```console
sudo pip install -r ~/environment/LAB03/03-COGNITO/requirements.txt
```

57. Review 'LAB03/03-COGNITO/cloudalbum/config.py'

* Set up **S3_PHOTO_BUCKET** value : Replace **cloudalbum-\<INITIAL\>** to exist value which created previous hands-on lab.

```python
import datetime
import os

class BaseConfig:
...
    # S3
    S3_PHOTO_BUCKET = os.getenv('S3_PHOTO_BUCKET', None)
    S3_PRESIGNED_URL_EXPIRE_TIME = int(os.getenv('S3_PRESIGNED_URL_EXPIRE_TIME', '3600'))

    # Cognito
    COGNITO_POOL_ID = os.getenv('COGNITO_POOL_ID', None)
    COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID', None)
    COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET', None)
...
```

* Check the values under ***# COGNITO***.
* The second parameter of **os.getenv** is the default value to use when the first parameter does not exist.

| COGNITO_POOL_ID | Copy and paste the pool ID you noted earlier. |
----|----
| COGNITO_CLIENT_ID | Copy and paste the App Client ID you noted earlier. |
| COGNITO_CLIENT_SECRET | Copy and paste the App Client Secret you noted earlier. |


 * These values are initialized from environment variables. You can specify these values in `shell.env` and load them as easily as before using the `source shell.env` command.

 * Here is required variables in `shell.env`. You can uncomment and specify your own values.
```console
# Required environment variables
export UPLOAD_FOLDER=/tmp
export FLASK_APP=cloudalbum/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=cloudalbum.config.DevelopmentConfig
export DDB_RCU=10
export DDB_WCU=10
export S3_PHOTO_BUCKET=
export S3_PRESIGNED_URL_EXPIRE_TIME=3600
export COGNITO_POOL_ID=
export COGNITO_CLIENT_ID=
export COGNITO_CLIENT_SECRET=
```

58. Before implement TODO #7, you need to review **LAB03/03-Cognito/backend/cloudalbum/database/model_ddb.py** file. Compare to the previous lab, there is only one table:Photo. It means from now **Cognito User pool replace original User table of DynamoDB**.

```python
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


* Review  **LAB03/03-Cognito/backend/cloudalbum/api/users.py**, and compare to the previous lab:   **LAB03/02-S3/backend/cloudalbum/api/users.py**. 

* Before using Cognito: **LAB03/02-S3/backend/cloudalbum/api/users.py**
```python 
	user = get_jwt_identity()
	add_token_to_set(get_raw_jwt())
```
* There was a **set to store expired-or blacklisted- token** of sign-out user's into your application memory. However, after using Cognito, you don't need to save blacklisted token at server-side anymore. All you need to do is bring Boto3 client and let the Cognito know which token is expired.

* After using Cognito: **LAB03/03-Cognito/backend/cloudalbum/api/users.py**
```python
	try:
	    client = boto3.client('cognito-idp')
	    response = client.global_sign_out(
	        AccessToken=token
	    )
```

61. We don't need User tables anymore. So, now we can **remove User table** in DynamoDB console.
<img src=./images/lab03-task3-delete-user-table.png width=800>



62. Now we can run unittest to check if our application is working properly.

* Before, run unittest you need to load environment variables for the application. You can check this `~/environment/LAB03/03-Cognito/backend/shell.env` file.

* You can also check `~/environment/LAB03/03-Cognito/backend/cloudalbum/config.py` file. Configure `S3_PHOTO_BUCKET` value and uncomment this. Before run `source shell.env`.

```console
# Required environment variables
export UPLOAD_FOLDER=/tmp
export FLASK_APP=cloudalbum/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=cloudalbum.config.DevelopmentConfig
export DDB_RCU=10
export DDB_WCU=10
export S3_PHOTO_BUCKET=
export S3_PRESIGNED_URL_EXPIRE_TIME=3600
export COGNITO_POOL_ID=
export COGNITO_CLIENT_ID=
export COGNITO_CLIENT_SECRET=
```
* Make sure, all required environment variables should set properly. (**S3_PHOTO_BUCKET, COGNITO_POOL_ID, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET**)

```console
source ~/environment/LAB03/03-Cognito/backend/shell.env
cd ~/environment/LAB03/03-Cognito/backend/cloudalbum/tests
```
* Run unittest like below.
```console
pytest -v -W ignore::DeprecationWarning
```
* Output
```console
=============================== test session starts ================================
platform linux -- Python 3.6.8, pytest-5.1.2, py-1.8.0, pluggy-0.13.0 -- /home/ec2-user/environment/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/ec2-user/environment/LAB03/03-Cognito/backend/cloudalbum/tests
plugins: cov-2.7.1
collected 37 items                                                                 

test_admin.py::TestAdminService::test_healthcheck PASSED                     [  2%]
test_admin.py::TestAdminService::test_ping PASSED                            [  5%]
test_config.py::TestDevelopmentConfig::test_app_is_development PASSED        [  8%]
test_config.py::TestDevelopmentConfig::test_cognito_client_id PASSED         [ 10%]
test_config.py::TestDevelopmentConfig::test_cognito_client_secret PASSED     [ 13%]
test_config.py::TestDevelopmentConfig::test_cognito_pool_id PASSED           [ 16%]
test_config.py::TestDevelopmentConfig::test_ddb_rcu PASSED                   [ 18%]
test_config.py::TestDevelopmentConfig::test_ddb_wcu PASSED                   [ 21%]
test_config.py::TestDevelopmentConfig::test_s3_bucket PASSED                 [ 24%]
test_config.py::TestTestingConfig::test_app_is_testing PASSED                [ 27%]
test_config.py::TestTestingConfig::test_cognito_client_id PASSED             [ 29%]
test_config.py::TestTestingConfig::test_cognito_client_secret PASSED         [ 32%]
test_config.py::TestTestingConfig::test_cognito_pool_id PASSED               [ 35%]
test_config.py::TestTestingConfig::test_ddb_rcu PASSED                       [ 37%]
test_config.py::TestTestingConfig::test_ddb_wcu PASSED                       [ 40%]
test_config.py::TestTestingConfig::test_s3_bucket PASSED                     [ 43%]
test_config.py::TestProductionConfig::test_app_is_production PASSED          [ 45%]
test_config.py::TestProductionConfig::test_cognito_client_id PASSED          [ 48%]
test_config.py::TestProductionConfig::test_cognito_client_secret PASSED      [ 51%]
test_config.py::TestProductionConfig::test_cognito_pool_id PASSED            [ 54%]
test_config.py::TestProductionConfig::test_ddb_rcu PASSED                    [ 56%]
test_config.py::TestProductionConfig::test_ddb_wcu PASSED                    [ 59%]
test_config.py::TestProductionConfig::test_s3_bucket PASSED                  [ 62%]
test_dynamodb.py::TestDynamoDBService::test_photo_table PASSED               [ 64%]
test_photos.py::TestPhotoService::test_delete PASSED                         [ 67%]
test_photos.py::TestPhotoService::test_get_mode_thumb_orig PASSED            [ 70%]
test_photos.py::TestPhotoService::test_list PASSED                           [ 72%]
test_photos.py::TestPhotoService::test_ping PASSED                           [ 75%]
test_photos.py::TestPhotoService::test_upload PASSED                         [ 78%]
test_s3.py::TestS3Service::test_bucket_availability PASSED                   [ 81%]
test_users.py::TestUserService::test_bad_signin PASSED                       [ 83%]
test_users.py::TestUserService::test_bad_signup PASSED                       [ 86%]
test_users.py::TestUserService::test_ping PASSED                             [ 89%]
test_users.py::TestUserService::test_signin PASSED                           [ 91%]
test_users.py::TestUserService::test_signout PASSED                          [ 94%]
test_users.py::TestUserService::test_signup PASSED                           [ 97%]
test_users.py::TestUserService::test_signup_duplicate_email PASSED           [100%]

=============================== 37 passed in 15.03s ================================
```

63. You can run CloudAlbum application like below after unittest.
  * for backend.
```console
cd ~/environment/LAB03/03-Cognito/backend
python manage.py run -h 0.0.0.0 -p 5000 
```
  * for frontend. (use another terminal in Cloud9)
```console
cd ~/environment/frontend/cloudalbum/
npm run serve
```

  * You can also refer to 
  [TASK 3. Connect to your application (Via SSH Tunneling)](LAB01.md#task-3-connect-to-your-application-(via-ssh-tunneling)) and [TASK 2. Look around current application and try run it.](LAB01.md#task-2.-look-around-current-application-and-try-run-it.)in LAB01.

64. Enjoy the CloudAlbum with DynamoDB, S3 and Cognito.
  * You can use `python manage.py seed_db` command to create test user easily.

<img src=./images/lab01-02.png width=700>


65. Examine Cognito management console.
<img src=./images/lab03-task3-cognito-users.png width=500>


* Stop your application. 
* You can stop both frontend and backend application by press `ctrl+c` in your Cloud9 Terminal.

Is it OK? Let's move to the next TASK.


## TASK 5. Go to X-ray

AWS [X-Ray](https://aws.amazon.com/xray/) helps developers analyze and debug production, distributed applications, such as those built using a microservices architecture. With X-Ray, you can understand how your application and its underlying services are performing to identify and troubleshoot the root cause of performance issues and errors. X-Ray provides an end-to-end view of requests as they travel through your application, and shows a map of your application’s underlying components. You can use X-Ray to analyze both applications in development and in production, from simple three-tier applications to complex microservices applications consisting of thousands of services.

<img src="./images/lab03-task4-x-ray-arc.png" width="600">

66. Install required Python packages for AWS X-Ray.
```console
sudo pip install -r ~/environment/LAB03/04-XRAY/requirements.txt
```

**Download and run the AWS X-Ray daemon on your AWS Cloud9 instance.**

67. Visit the AWS X-Ray daemon documentation link below:
* https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html

68. On the documentation page, scroll down until you see a link to **Linux (executable)-aws-xray-daemon-linux-2.x.zip (sig).** Right-click the link and copy the link address.

69. In your AWS **Cloud9 instance terminal**, type the command below to go to your home directory.
```console
cd ~
```

70. Type wget and paste the AWS X-Ray daemon hyperlink address that you copied. The command should look like the example below.
```console
wget https://s3.dualstack.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-3.x.zip
```

71. Unzip the AWS X-Ray daemon by typing the command below. Make sure that the name of the .zip file matches the one in the command below.
```console
unzip aws-xray-daemon-linux-3.x.zip
```

72. Run the AWS X-Ray daemon by typing the command below. The X-Ray daemon buffers segments in a queue and uploads them to X-Ray in batches. 

```console
./xray
```

* **Now, X-Ray daemon works and ready to use X-Ray to analyze applications. Keep this terminal until complete this hands-on lab. Because we'll explore X-ray console to check the api call logs.**


### TODO #9

73. Review TODO #9 which is in **LAB03/04-XRAY/cloudalbum/backend/__init__.py** file.

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

74. Now we can run unittest to check if our application is working properly.

* **NOTE:** The X-ray daemon must be alive. (refer to step 72) **Because we'll explore X-ray console to check the api call logs.**

* Before, run unittest you need to load environment variables for the application. 

```console
# Required environment variables
export UPLOAD_FOLDER=/tmp
export FLASK_APP=cloudalbum/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=cloudalbum.config.DevelopmentConfig
export DDB_RCU=10
export DDB_WCU=10
export S3_PHOTO_BUCKET=
export S3_PRESIGNED_URL_EXPIRE_TIME=3600
export COGNITO_POOL_ID=
export COGNITO_CLIENT_ID=
export COGNITO_CLIENT_SECRET=
```
* Make sure, all required environment variables should set properly. (**S3_PHOTO_BUCKET, COGNITO_POOL_ID, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET**)

* You can also check `~/environment/LAB03/04-Xray/backend/cloudalbum/config.py` file.


```console
source ~/environment/LAB03/04-Xray/backend/shell.env
cd ~/environment/LAB03/04-Xray/backend/cloudalbum/tests
```
* Run unittest like below.
```console
pytest -v -W ignore::DeprecationWarning
```
* Output
```console
============================== test session starts ==============================
platform linux -- Python 3.6.8, pytest-5.1.2, py-1.8.0, pluggy-0.13.0 -- /home/ec2-user/environment/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/ec2-user/environment/LAB03/04-Xray/backend/cloudalbum/tests
plugins: cov-2.7.1
collected 37 items                                                              

test_admin.py::TestAdminService::test_healthcheck PASSED                  [  2%]
test_admin.py::TestAdminService::test_ping PASSED                         [  5%]
test_config.py::TestDevelopmentConfig::test_app_is_development PASSED     [  8%]
test_config.py::TestDevelopmentConfig::test_cognito_client_id PASSED      [ 10%]
test_config.py::TestDevelopmentConfig::test_cognito_client_secret PASSED  [ 13%]
test_config.py::TestDevelopmentConfig::test_cognito_pool_id PASSED        [ 16%]
test_config.py::TestDevelopmentConfig::test_ddb_rcu PASSED                [ 18%]
test_config.py::TestDevelopmentConfig::test_ddb_wcu PASSED                [ 21%]
test_config.py::TestDevelopmentConfig::test_s3_bucket PASSED              [ 24%]
test_config.py::TestTestingConfig::test_app_is_testing PASSED             [ 27%]
test_config.py::TestTestingConfig::test_cognito_client_id PASSED          [ 29%]
test_config.py::TestTestingConfig::test_cognito_client_secret PASSED      [ 32%]
test_config.py::TestTestingConfig::test_cognito_pool_id PASSED            [ 35%]
test_config.py::TestTestingConfig::test_ddb_rcu PASSED                    [ 37%]
test_config.py::TestTestingConfig::test_ddb_wcu PASSED                    [ 40%]
test_config.py::TestTestingConfig::test_s3_bucket PASSED                  [ 43%]
test_config.py::TestProductionConfig::test_app_is_production PASSED       [ 45%]
test_config.py::TestProductionConfig::test_cognito_client_id PASSED       [ 48%]
test_config.py::TestProductionConfig::test_cognito_client_secret PASSED   [ 51%]
test_config.py::TestProductionConfig::test_cognito_pool_id PASSED         [ 54%]
test_config.py::TestProductionConfig::test_ddb_rcu PASSED                 [ 56%]
test_config.py::TestProductionConfig::test_ddb_wcu PASSED                 [ 59%]
test_config.py::TestProductionConfig::test_s3_bucket PASSED               [ 62%]
test_dynamodb.py::TestDynamoDBService::test_photo_table PASSED            [ 64%]
test_photos.py::TestPhotoService::test_delete PASSED                      [ 67%]
test_photos.py::TestPhotoService::test_get_mode_thumb_orig PASSED         [ 70%]
test_photos.py::TestPhotoService::test_list PASSED                        [ 72%]
test_photos.py::TestPhotoService::test_ping PASSED                        [ 75%]
test_photos.py::TestPhotoService::test_upload PASSED                      [ 78%]
test_s3.py::TestS3Service::test_bucket_availability PASSED                [ 81%]
test_users.py::TestUserService::test_bad_signin PASSED                    [ 83%]
test_users.py::TestUserService::test_bad_signup PASSED                    [ 86%]
test_users.py::TestUserService::test_ping PASSED                          [ 89%]
test_users.py::TestUserService::test_signin PASSED                        [ 91%]
test_users.py::TestUserService::test_signout PASSED                       [ 94%]
test_users.py::TestUserService::test_signup PASSED                        [ 97%]
test_users.py::TestUserService::test_signup_duplicate_email PASSED        [100%]

============================== 37 passed in 15.14s ==============================
```

75. You can run CloudAlbum application like below after unittest.
  * for backend.
```console
cd ~/environment/LAB03/04-Xray/backend
python manage.py run -h 0.0.0.0 -p 5000 
```
  * for frontend. (use another terminal in Cloud9)
```console
cd ~/environment/frontend/cloudalbum/
npm run serve
```

  * You can also refer to 
  [TASK 3. Connect to your application (Via SSH Tunneling)](LAB01.md#task-3-connect-to-your-application-(via-ssh-tunneling)) and [TASK 2. Look around current application and try run it.](LAB01.md#task-2.-look-around-current-application-and-try-run-it.)in LAB01.

76. Enjoy the CloudAlbum with DynamoDB, S3, Cognito and X-ray.
<img src=./images/lab01-02.png width=700>


77. Examine X-Ray Console dashboard
* AWS X-Ray: Service map
<img src=images/lab03-task4-x-ray-service-map.png width=500>
* AWS X-Ray: Traces
<img src=images/lab03-task4-x-ray-traces.png width=500>

78. Stop your application. 
* You can stop both frontend and backend application by press `ctrl+c` in your Cloud9 Terminal.

In this LAB, Amazon RDS and EFS have been replaced by the serverless services Amazon DynamoDB and S3. But still our application runs on EC2. In the next hands-on lab, we will migrate our application to Lambda and API Gateway.



# Congratulation! You completed LAB03.

## LAB GUIDE LINKS
* [Lab 1: CloudAlbum with 3-tier Architecture](LAB01.md)
* [Lab 2: CloudAlbum with 3-tier architecture and high availability](LAB02.md)
* [Lab 3: CloudAlbum with Serverless Architecture - Part 1](LAB03.md)
* [Lab 4: CloudAlbum with Serverless Architecture - Part 2](LAB04.md)
