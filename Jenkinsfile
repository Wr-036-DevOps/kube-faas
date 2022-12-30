pipeline {
    agent {
      node {
        label "master" 
      }    
    }
    
    environment {
        gw     = credentials('k8s_gateway')
        
    }
    
    stages {
      stage('Build') {
        steps {
          sh 'faas-cli build -f ./kachi-fxn.yml'
        }
      }

      stage("Push to Docker") {
        steps {
          withCredentials([string(credentialsId: 'Docker_Hub_Password', variable: 'PASSWORD')]) {
          sh 'docker login -u akmba -p $PASSWORD'
          sh 'faas-cli push -f ./kachi-fxn.yml'
        }}
      }

      stage('Kubernetes Deployment') {
        steps {
          withCredentials([[
                $class: 'AmazonWebServicesCredentialsBinding',
                credentialsId: "AWS_CREDENTIALS",
                accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]){ 
          sh ''' 
              PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo) && \
              echo $PASSWORD | faas-cli login --username admin --password-stdin $PASSWORD -gateway $gw
              faas-cli deploy -f ./kachi-fxn.yml -gateway $gw
          '''
        }
      }
    } 
  }
}