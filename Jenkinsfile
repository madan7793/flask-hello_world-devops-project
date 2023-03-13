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
               sh 'ssh madan192.168.43.189 kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/deployment.yaml'
               sh 'ssh madan192.168.43.189 kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/service.yaml'
           }
       }
   }
}