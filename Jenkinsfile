#!/usr/bin/env groovy

pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://172.210.1.148/:9000'
        SONARQUBE_TOKEN = credentials('OpeEmailAppCredential')
        SONARSCANNER_HOME = tool 'sonarqube-scanner' // Tool name configured in Jenkins Global Tool Configuration
        MAX_ALLOWED_BUGS = 1
        JENKINS_API_TOKEN = credentials("JENKINS_API_TOKEN")
       // email_app_token =  credentials("email_app_token")
        email_app_token = 5b1fa8a7a697d8f8eee67fce6b30a4e0
    }
 
    stages {

        stage('Checkout') {
            steps {
                script {
                    // Clean workspace before checking out
                    deleteDir()

                    // Checkout the code from the GitHub repository
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'emailApp']], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/EzeChinedumUchenna/emailApp.git']]])
                }
            }
        }

        stage("image") {
            steps {
                script {
                    // Navigate to the directory containing the Dockerfile
                    dir('emailApp') {
                        // Build the Docker image
                        sh 'docker build -t nedumacr.azurecr.io/nedumpythonapp:$BUILD_NUMBER .'
                  }
                }
            }
        }
        stage('SonarQube Scan') {
            steps {
                script {
                    // Use the configured SonarScanner installation
                    withSonarQubeEnv('sonarqube-server') {
                        sh """
                            ${SONARSCANNER_HOME}/bin/sonar-scanner \
                            -Dsonar.projectKey=your_project_key \
                            -Dsonar.projectName=YourProjectName \
                            -Dsonar.projectVersion=1.0 \
                            -Dsonar.sources=. \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.python.xunit.reportPath=test-reports.xml
                        """
                    }
                }
            }
        }
    stage('SonarQube Quality Gate') {
      steps {
        script {
         timeout(time: 3, unit:'MINUTES') {
             waitForQualityGate abortPipeline: false, credentialsId: 'OpeEmailAppCredential'
          }
        }
     }
   }
    stage('Push to ACR') {
            steps {
                // Push the Docker image to Azure Container Registry
                script {
                    echo "deploying image to ACR ...."
                    withCredentials([usernamePassword(credentialsId: 'azure_acr', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        sh "echo $PASS | docker login -u $USER --password-stdin nedumacr.azurecr.io"
        sh 'docker push nedumacr.azurecr.io/nedumpythonapp:$BUILD_NUMBER'
                }
            }
        }
        //stage('Deploy to Azure') {
          //  steps {
                // Add your deployment steps here
                // This could include updating a Kubernetes deployment, triggering a release, etc.
                // Example: deploy to Azure Kubernetes Service (AKS)
          //      script {
                    // Use Azure CLI or Kubernetes CLI to update deployment
            //        sh "az aks update -n your-aks-cluster -g your-resource-group --image ${ACR_SERVER}/${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
              //  }
            //}
        //}
    }
    stage('Trivy Scan') {
            steps {
                    script {
                        //def trivyOutput = sh(script: 'trivy image --severity HIGH --exit-code 1 nedumacr.azurecr.io/nedumpythonapp:$BUILD_NUMBER', returnStdout: true)
                        def trivyOutput = sh(script: 'trivy image --severity HIGH nedumacr.azurecr.io/nedumpythonapp:$BUILD_NUMBER', returnStdout: true) // We remove the "--exit-code 1" to allow the pipeline to continue even when he severity id high
                        echo "Trivy scan results: ${trivyOutput}"
                        // In the above code snippet, the trivy command scans the container image for vulnerabilities with High severity and returns an exit code of 1 if any are found. 
                        // The --exit-code 1 option causes the pipeline process to stop when High severity vulnerabilities are detected. Replace <IMAGE_NAME> with the name of your container image.
                    }
                }
            }
   stage('Clean Up Artifact') {
            steps {
                    script {
                        sh 'docker rmi nedumacr.azurecr.io/nedumpythonapp:$BUILD_NUMBER'
                    }
            }
   }
   stage('Trigger CD pipeline') {
            steps {
                    script {
                       // sh "curl -v -k --user userman:${JEKINS_API} -X POST -H 'cache-control: no cache' -H token=TOKEN_NAME'
                        sh "curl -v -k --user chinedum:${JENKINS_API_TOKEN} -X POST -H 'cache-control: no-cache' -H 'content-type: application/x-www-form-urlencoded' --data 'BUILD_NUMBER=${BUILD_NUMBER}' '20.121.45.30:8080/job/emialApp-CD-Job/buildWithParameters?token=email_app_token'"
                    }
            }
   }     
}
}
