Prerequisites

Linux machine
Python
Flask
Docker
Git and Github
Jenkins
Kubernetes
Steps in the CI/CD pipeline


Create a "Hello world" Flask application


from flask import Flask
import os
app = Flask(__name__)
@app.route("/")
def hello():
  return "Hello world"
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(debug=True, host='0.0.0.0', port=port)


dependencies python installed for running my flask_app

click==8.0.3
colorama==0.4.4
Flask==2.0.2
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.0.1
Werkzeug==2.0.2
gunicorn==20.1.0


Tested on Local Machine
I used py-env for running flask app on Local Machine

First i installed -  sudo  apt install python3.8-venv
python3 -m venv venv


Dockerise the application
FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD ["app.py" ]


Test the code locally by building docker image and running it
Create a github repository  (“flask-hello_world-devops-project”) and push code to it


GitHub Repository : https://github.com/madan7793/flask-hello_world-devops-project.git

Start a Jenkins server on a host

Write a Jenkins pipeline to build, test and push the docker image to Dockerhub.


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
      stage('Test') {
          steps {
              echo 'Testing..'
              sh 'docker stop $CONTAINER_NAME || true'
              sh 'docker rm $CONTAINER_NAME || true'
              sh 'docker run --name $CONTAINER_NAME $DOCKER_HUB_REPO'
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




Pushed the Docker image on DockerHub Repository
DockerHubRepository:- https://hub.docker.com/repository/docker/madanmohan7793/flask_app_image/general

Deployed app on kubernetes using Jenkins CI-CD
used  NodePort service Type




