pipeline {
    agent {
      node {
        label "master"
      } 
    }
    
    stages {
      stage('Build') {
        steps {
          sh 'cd kube-faas'   
          sh 'faas-cli build -f ./kachi-fxn.yml'
        }
      }

      stage("Push to Docker") {
        steps {
          sh 'faas-cli push -f ./kachi-fxn.yml'
        }
      }

      stage('Kubernetes Deployment') {
        steps {
          sh 'faas-cli deploy -f ./kachi-fxn.yml'
        }
      }
    } 
  }
