pipeline {
   agent any
  
   environment {
       DOCKER_HUB_REPO = "madanmohan7793/flask_app_image"
       CONTAINER_NAME = "flask-hello-world"
       DOCKERHUB_CREDENTIALS=credentials('dockerhub_credential')
   }
  
   stages {
       /* We do not need a stage for checkout here since it is done by default when using "Pipeline script from SCM" option. */
      
       }
       stage('Deploy') {
           steps {
               echo 'Deploying....'
               sh  kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/deployment.yaml'
               sh  kubectl apply -f /var/lib/jenkins/workspace/flask-hello-world-app/service.yaml'
           }
       }
   
}
