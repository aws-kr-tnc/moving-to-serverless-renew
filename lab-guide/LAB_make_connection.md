
1. Now, let's run back-end application server. To run the back-end application server we will use a Cloud9 terminal.

* First, set up environment variables.
```console
export FLASK_ENV=development
export APP_SETTINGS=cloudalbum.config.DevelopmentConfig
```

* Then, run following command
```console
cd ~/environment/moving-to-serverless-renew/LAB03/<your current lab name:e.g.01-DDB>/backend
python manage.py run -h 0.0.0.0 -p 5000
```

* And now, you can see the following messages on your terminal.
	
```console
(venv) demo:~/environment/moving-to-serverless-renew/LAB01/backend (master) $ python3 manage.py run -h 0.0.0.0 -p 5000
[2019-08-25 13:07:17,022] INFO in __init__: Create database tables
Create database tables
[2019-08-25 13:07:17,023] INFO in manage: SQLALCHEMY_DATABASE_URI: sqlite:////tmp/sqlite_dev.database
SQLALCHEMY_DATABASE_URI: sqlite:////tmp/sqlite_dev.database
[2019-08-25 13:07:17,023] INFO in manage: UPLOAD_FOLDER: /home/ec2-user/environment/moving-to-serverless-renew/LAB01/backend/upload
UPLOAD_FOLDER: /home/ec2-user/environment/moving-to-serverless-renew/LAB01/backend/upload
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

2. Let's call a simple api to check if the back-end application ran successfully. We'll use httpie to test it.

```console
http localhost:5000/users/ping
```
* Now you can see similar messages below.

```console
(venv) demo:~/environment $ http localhost:5000/users/ping                                                                                                                                                        
HTTP/1.0 200 OK
Access-Control-Allow-Origin: *
Content-Length: 38
Content-Type: application/json
Date: Sun, 25 Aug 2019 13:07:32 GMT
Server: Werkzeug/0.15.5 Python/3.6.8

{
    "Message": {
        "msg": "pong!"
    },
    "ok": true
}
```


3. Now, let's run front-end application server. To run the front-end application we need to run front-end application server.

```console
npm run serve
```

* And then you can see similar messages below.

```console
...
Use Ctrl+C to close it

  App running at:
  - Local:   http://localhost:8080/ 
  - Network: http://172.31.4.231:8080/

  Note that the development build is not optimized.
  To create a production build, run npm run build.

```

## Connect to your application (Via SSH Tunneling)

Cloud9 has preview feature to support yout application development.
 * You can refer following document : https://docs.aws.amazon.com/cloud9/latest/user-guide/app-preview.html

for convenience, we will use **SSH tunnel** to access our application in Cloud9 instance.

4. Add your public key to `.ssh/authorized_keys`.

<img src=./images/lab01-task3-ssh-tunnel.png width=1000>

* In your MAC/Linux terminal, type the command below to get the public portion from **your existing any key pair .pem** file. Make sure to replace YOUR_KEY with the name of the key pair .pem file

```console
ssh-keygen -f <YOUR_KEY.pem> -y
```

* The output looks like the example below. Copy the output of your command.
```console
ssh-rsa
ASDASDASDASDAyc2EAAAADAQABAAABAQDWGRZsPraV6v4UqfZTFKAXK9bhjWVkONEKyAA1CeOkxSN+9WdY7gKgjbPOeUx3LFqRudBvSrP+eKTtthPrl Nx9UBvXniVK252i4h0xnIcrRO1PUpq0EzyqX+n3u2YwytT+on6x98PRjtD4oCKyfFviWBqnRHtWvRre8CWhULuJrmUeo2aPrVTPXo/TwJpZupXv63YyUMPC 2wyDMDsKNZhsqUedkJ8575PGXCg9gEkPg2ulR8NUrzDSfbXIrZLgCcIziwDQ0dA9B28OAQ9saPyXYzrZF1ZmCxKgzSHHiKdBAJ0E/X/s53N5Hg04SIWy4D4lMT 9g+AZG38YPNq68mo4b
```

* In your AWS Cloud9 instance, on the left pane, click the **Settings** icon. Click **Show Home in Favorites** and **Show Hidden Files** as shown in the screenshot below.
<img src=./images/lab01-05.png width=500>

* This should display the `.ssh` folder in the tree view.

* Expand the .ssh folder and open the **authorized_keys** file.

* Paste the public key you copied earlier in the authorized_keys file. **Important:** Make sure to paste the public key below the message in the authorized_keys file as shown below. **Do not delete or overwrite** the public key already present in the file. Deleting or overwriting the existing public key will make your Cloud9 instance unusable.

```console
...
...
 #
 # Add any additional keys below this line
 #
```
* Save the **authorized_keys** file. By updating this file, you are telling your AWS Cloud9 instance to allow connections that authenticate with the matching private key.

**NOTE:** You also can paste it using cli command like below. (Paste public key then press CTRL+D for EOF)

```console
cat >> ~/.ssh/authorized_keys
ssh-rsa CXCAAB3Nzaxxyc2EAAAADAQABAAABAQDThHERqJJMcZqitA5DZ35j41UFE0zIO5XxVqElCHNHUXYnmffqFNyTFkfpkHAWsR5zGMnR5I46eZazu4sWNcg3LZx937/STOfN4TCzps/uuooHx/p3whGXIFqsz25Xq1RzI/LsFiSRm3+/I1E482pss3OgCXALR/rF9g7Mud1frt9POq82Zg0R1YHB5hCK6Ldx3U3AnFxdViKHVnDgVijAYO+ua1MFtaSn+FqYoXbMniFiQpOJz2ZTvM/ZhwvfAYJkJPYwQ+7T99pIEb0L/pLecaFkxUcbAiwzW6L79bKAQYwA7vEzI4ndqhyLKwIzadVJnog1hRs0ItiUqDOSLYLN sungshik@8c85904c36cf.ant.amazon.com

```

5. Open TCP port 22 of Cloud9 instance to your current public IP.

* Check the public IP address you are using now. You can access following site to get current public IP.
  * https://checkip.amazonaws.com/ 

  <img src=./images/lab01-check-myip.png width=500>

* Keep your IP address for later use. Now, open your new terminal in the Cloud9.

  <img src=./images/lab01-open-terminal.png width=500>

* Run, below command. To add new ingress Security Group rule for SSH connection.
```console
SG_NAME=`curl -s http://169.254.169.254/latest/meta-data/security-groups`
SG_ID=`aws ec2 describe-security-groups --group-names $SG_NAME --query 'SecurityGroups[*].[GroupId]' --output text`
```

* Before run below command, you should replace  `<YOUR_IP>` like `61.79.225.xxx`.
```console
aws ec2 authorize-security-group-ingress \
--group-id $SG_ID \
--protocol tcp \
--port 22 \
--cidr <YOUR_IP>/32

```

* You can check the result via below command. (61.79.xxx.xxx/32)
```console
aws ec2 describe-security-groups --group-ids $SG_ID --query "SecurityGroups[].IpPermissions[].IpRanges"
[
    [
        {
            "CidrIp": "13.250.xxx.xxx/27"
        }, 
        {
            "CidrIp": "13.250.xxx.xxx/27"
        }, 
        {
            "CidrIp": "61.79.xxx.xxx/32"
        }
    ]
]
```


6. Make a SSH connection with tunneling.

* Let's get public IP of Cloud9. Try below command 
in your Cloud9 terminal and keep the IP. 
```console
ec2-metadata -v
public-ipv4: 54.169.xxx.xxx
```

* Try to SSH tunneling like this

* **NOTE:** Make sure **your Cloud9 instance Security group port 22** is opened for SSH tunneling.

```console
ssh -i <YOUR_KEY.pem> -L 8080:localhost:8080 -L 5000:localhost:5000 ec2-user@<CLOUD9 PUBLIC-IP>
```

7. Connect to your front-end application using your browser.
 * http://localhost:8080/
<img src="./images/lab01-08.png" width=500>


8. Our backend application support SWAGGER. Now you can see SWAGGER interface of backend application.

* Swagger is an open-source software framework backed by a large ecosystem of tools that helps developers design, build, document, and consume RESTful Web services. Swagger also allows you to understand and test your backend api specifically.

  * User API : http://localhost:5000/users/swagger/
<img src="./images/lab01-swagger-user.png" width=500>

  * Photo API : http://localhost:5000/photos/swagger/
<img src="./images/lab01-swagger-photo.png" width=500>


9. Take a look around and perform test.
<img src="./images/lab01-02.png" width=800>

* Sign in / up
* Upload Sample Photos
* **Download sample images here** (EXIF data included) 
  *  https://d2r3btx883i63b.cloudfront.net/temp/sample-photo.zip
* Look your Album
* Find photos with Search tool
* Check the Photo Map