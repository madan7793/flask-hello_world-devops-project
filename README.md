# flask-hello_world-devops-project
Build and deploy code a simple flask application using Jenkins and Kubernetes
 
In this project, we are going to build a simple [CI/CD](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment) pipeline from scratch using tools like Flask, Docker, Git, Github, Jenkins and Kubernetes.
 
## Prerequisites
 
* Python
* Flask
* Docker
* Git and Github
* Jenkins
* Kubernetes
* Linux machine
 
## Steps in the CI/CD pipeline
1. Create a "Hello world" Flask application
2. Write basic test cases
3. Dockerise the application
4. Test the code locally by building docker image and running it
5. Create a github repository and push code to it
6. Start a Jenkins server on a host
7. Write a Jenkins pipeline to build, test and push the docker image to Dockerhub.
8. Set up Kubernetes on a host using [Minikube](https://minikube.sigs.k8s.io/docs/start/)
9. Create a Kubernetes deployment and service for the application.
10. Use Jenkins to deploy the application on Kubernetes
 
## Project structure
 
* app.py - Flask application which will print "Hello world" when we run it
* test.py - Test cases for the application
* requirements.txt - Contains dependencies for the project
* Dockerfile - Contains commands to build and run the docker image
* Jenkinsfile - Contains the pipeline script which will help in building, testing and deploying the application
* deployment.yaml - [Kubernetes deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) file for the application
* service.yaml - [Kubernetes service](https://kubernetes.io/docs/concepts/services-networking/service/) file for the application

## Create a project repository on Github
 
Login to my github account and create a new repository. Do make sure that we have given a unique name for the repository. It's good to add a README file.

## Clone the repository on my system
 
Go to my Github repository. Click on the "Code" section and note down the HTTPS url for the project.
 
 
Open terminal on my local machine(Desktop/laptop) and run the below commands.
 
```
git clone https://github.com/madan7793/flask-hello_world-devops-project.git 
cd flask-hello_world-devops-project
```
 
Run ls command and we should be able to see a local copy of the github repository.

## Set up virtual Python environment
 
Setting up a [virtual Python environment](https://docs.python.org/3/library/venv.html) will help in testing the code locally and also collecting all the dependencies.
 
```bash
python3 -m venv venv # Create the virtual env named venv
source venv/bin/activate # Activate the virtual env
```

## Create a Flask application
 
Install the flask module.
 
```bash
pip install flask
```
 
Create a new file named "app.py" and add the below code.
 
```python
from flask import Flask
import os
 
app = Flask(__name__)
 
 
@app.route("/")
def hello():
   return "Hello world"
 
 
if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5000))
   app.run(debug=True, host='0.0.0.0', port=port)
```

The above code when run will start a web server on port number 5000. 
 
```bash
python app.py
```

Open my browser and visit [](http://127.0.0.1:5000). we should see "Hello world" printed on the browser.

## Dockerise the application
 
Install docker on my system. Follow [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
 
Create a file named "Dockerfile" and add the below code.
 
```
FROM python:3.6
COPY app.py test.py /app/
WORKDIR /app
RUN pip install flask pytest flake8 # This downloads all the dependencies
CMD ["python", "app.py"]
```
 
Build the docker image.
 
```bash
docker build -t flask-hello-world .
```
 
Run the application using docker image.
 
```bash
docker run -it -p 5000:5000 flask-hello-world
```

Push the image to dockerhub. we will need an account on docker hub for this.
 
```bash
docker login # Login to docker hub
docker tag latest madanmohan7793/flask_app_image 
docker push madanmohan7793/flask_app_image

Till now, we haven't pushed the code to our remote repository. Let's try some basic git commands to push the code.
 
```bash
git add .
git commit -m "flask-app-assignment"
git push origin master
```

## Installed Jenkins

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
/usr/share/keyrings/jenkins-keyring.asc > /dev/null
 
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
/etc/apt/sources.list.d/jenkins.list > /dev/null
 
sudo apt-get update
sudo apt install openjdk-11-jre
sudo apt-get install jenkins

# Install docker and add jenkins user to docker group

sudo apt install docker.io
sudo usermod -aG docker jenkins
sudo service jenkins restart

## Create a Jenkins pipeline
 below code in the pipeline section


pipeline {
   agent any
  
   environment {
       DOCKER_HUB_REPO = "madanmohan7793/flask_app_image"
       CONTAINER_NAME = "flask-hello-world"
       DOCKERHUB_CREDENTIALS=credentials('dockerhub_credential')
   }
  
   stages {
       /* We do not need a stage for checkout here since it is done by default when using "Pipeline script from SCM" option. */
      
       stage('Build') {
           steps {
               echo 'Building..'
               sh 'docker image build -t $DOCKER_HUB_REPO:latest .'
           }
       }
       stage('Push') {
           steps {
               echo 'Pushing image..'
               sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
               sh 'docker push $DOCKER_HUB_REPO:latest'
           }
       }
       stage('Deploy') {
           steps {
               echo 'Deploying....'
               sh 'scp -r -o StrictHostKeyChecking=no deployment.yaml service.yaml madan@192.168.43.189:~/'
               sh 'ssh madan@192.168.43.189 kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/deployment.yaml'
               sh 'ssh madan@192.168.43.189 kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/service.yaml'
           }
       }
   }
}



## Installed Kubernetes 

```bash
# https://minikube.sigs.k8s.io/docs/start/
 
# Install docker for managing containers
sudo apt-get install docker.io
 
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
 
# Add the current USER to docker group
sudo usermod -aG docker $USER && newgrp docker
 
# Start minikube cluster
minikube start
 

 Created a new file named "deployment.yaml"

 apiVersion: apps/v1
kind: Deployment
metadata:
 name: flask-hello-world-deployment # name of the deployment
 
spec:
 template: # pod defintion
   metadata:
     name: flask-hello-world # name of the pod
     labels:
       app: flask-hello-world
       tier: frontend
   spec:
     containers:
       - name: flask-hello-world
         image: madanmohan7793/flask-hello-world:flask-hello-world
 replicas: 3
 selector: # the pods which needs to be in the replicaset
   matchLabels:
     app: flask-hello-world
     tier: frontend


 Test the deployment manually by running the following command:
 
```bash
$ kubectl apply -f deployment.yaml

madan@madan:~$ kubectl get deployment
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
flask-hello-world-deployment   3/3     3            3           3h41m


Created a new file named "service.yaml" and add the following code

apiVersion: v1
kind: Service
metadata:
 name: flask-hello-world-service-nodeport       # name of the service
spec:
 type: NodePort        # Used for accessing a port externally
 ports:
   - port: 5000 # Service port
     targetPort: 5000 # Pod port, default: same as port
     nodePort: 30008 # Node port which can be used externally, default: auto-assign any free port
 selector: # Which pods to expose externally ?
   app: flask-hello-world
   tier: frontend



```bash
$ kubectl apply -f service.yaml

madan@madan:~$ kubectl get svc
NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
flask-hello-world-service-nodeport   NodePort       10.98.163.110   <none>        5000:30008/TCP   3h43m
kubernetes                           ClusterIP      10.96.0.1       <none>        443/TCP          14h
service-load-balancer                LoadBalancer   10.105.44.179   <pending>     8765:32257/TCP   65m


 created Both type of Service NodePort and LoadBalancer 


## Deploy using jenkins on kubernetes

First, we will add our docker hub credential in jenkins. This is needed as we have to first push the docker image before deploying on kubernetes.
 
Open jenkins credentials page.
 
 Click on 'global'.
 Add the credentials for docker hub account.

 We will now modify our Jenkinsfile in the project to push the image and then deploy the application on kubernetes.

 pipeline {
   agent any
  
   environment {
       DOCKER_HUB_REPO = "madanmohan7793/flask_app_image"
       CONTAINER_NAME = "flask-hello-world"
       DOCKERHUB_CREDENTIALS=credentials('dockerhub_credential')
   }
  
   stages {
       /* We do not need a stage for checkout here since it is done by default when using "Pipeline script from SCM" option. */
      
       stage('Build') {
           steps {
               echo 'Building..'
               sh 'docker image build -t $DOCKER_HUB_REPO:latest .'
           }
       }
       stage('Push') {
           steps {
               echo 'Pushing image..'
               sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
               sh 'docker push $DOCKER_HUB_REPO:latest'
           }
       }
       stage('Deploy') {
           steps {
               echo 'Deploying....'
               sh 'scp -r -o StrictHostKeyChecking=no deployment.yaml service.yaml madan@192.168.43.189:~/'
               sh 'ssh madan@192.168.43.189 kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/deployment.yaml'
               sh 'ssh madan@192.168.43.189 kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/service.yaml'
           }
       }
   }
}



## when  Kubernetes host different from the jenkins host 

In case we have set up kubernetes on a different virtual machine, we will need to ssh to this machine from jenkins machine, copy the deployment and service files and then run kubernetes commands.

Create a ssh key pair on jenkins server.
 
```bash
$ cd ~/.ssh # We are on jenkins server
$ ssh-keygen -t rsa # select the default options
$ cat id_rsa.pub # Copy the public key

Add the public key we created to authorized_keys on kubernetes server.
 
```bash
$ cd ~/.ssh # We are on kubernetes server
$ echo "<public key>" >> authorized_keys


Modify the 'Deploy' section of Jenkinsfile. Replace <username> and <ip address> with the username and ip address of kubernetes host respectively.
 
```
stage('Deploy') {
   steps {
       echo 'Deploying....'
       sh 'scp -r -o StrictHostKeyChecking=no deployment.yaml service.yaml < username>@<ip address>:~/'
 
       sh 'ssh <username><ip address> kubectl apply -f ~/deployment.yaml'
       sh 'ssh <username><ip address> kubectl apply -f ~/service.yaml'
   }
}
```

Commit the code. Build the pipeline again on Jenkins server.


