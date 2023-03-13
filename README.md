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

## Clone the repository on your system
 
Go to your Github repository. Click on the "Code" section and note down the HTTPS url for the project.
 
 
Open terminal on your local machine(Desktop/laptop) and run the below commands.
 
```
git clone https://github.com/madan7793/flask-hello_world-devops-project.git 
cd flask-hello_world-devops-project
```
 
Run ls command and you should be able to see a local copy of the github repository.

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

Open your browser and visit [](http://127.0.0.1:5000). You should see "Hello world" printed on the browser.

## Dockerise the application
 
Install docker on your system. Follow [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
 
Create a file named "Dockerfile" and add the below code.
 
```
FROM python:3.6
MAINTAINER Shivam Mitra "shivamm389@gmail.com" # Change the name and email address
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

Push the image to dockerhub. You will need an account on docker hub for this.
 
```bash
docker login # Login to docker hub
docker tag latest madanmohan7793/flask_app_image # Replace <shivammitra> with your docker hub username
docker push madanmohan7793/flask_app_image