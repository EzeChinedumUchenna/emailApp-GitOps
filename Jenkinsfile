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
        email_app_token = "5b1fa8a7a697d8f8eee67fce6b30a4e0"
        APP_NAME = "nedumacr.azurecr.io/nedumpythonapp"
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


        
  /** stage('Trigger CD pipeline') {
            steps {
                    script {
                       // sh "curl -v -k --user userman:${JEKINS_API} -X POST -H 'cache-control: no cache' -H token=TOKEN_NAME'
                        sh "curl -v -k --user chinedum:${JENKINS_API_TOKEN} -X POST -H 'cache-control: no-cache' -H 'content-type: application/x-www-form-urlencoded' --data 'BUILD_NUMBER=${BUILD_NUMBER}' '20.121.45.30:8080/job/emialApp-CD-Job/buildWithParameters?token=email_app_token'"
                    }
            }
   }  

} **/
     stage('Trigger CD pipeline') {
            steps {
                    script {
                      
                       withCredentials([usernamePassword(credentialsId: 'github_Credential', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    // First we are going to attach a metadata to our commit. Like email and username, else Jenkins will complain. This is very important and a must-have at first commit but can be remove aftr that.
                        sh 'cd emailApp'
                        sh 'git init .'
                        sh 'git config user.email "nedum_jenkins@gmail.com"' 
                        sh 'git config user.name "jenkins"'
                    // Note can set the above globally for all the project by adding '--global'
                    // sh 'git config --global user.email "nedum_jenkins@gmail.com"' 
                    // sh 'git config --global user.name "nedum_jenkins"' 
                    // we want git to print out the following information
                        sh 'git status'
                        sh 'git branch'
                        sh 'git config --list'

                    // Because my Github Password contain special character @, I will need to encode it else it wont work with Jenkins.
                        //def encodedPassword = URLEncoder.encode(PASS, "UTF-8")

                        // Set the Git remote URL with the encoded password
                        sh "git remote -v | grep origin || git remote add origin https://${USER}:${PASS}@github.com/EzeChinedumUchenna/emailApp-GitOps.git"
                        sh "git remote set-url origin https://${USER}:${PASS}@github.com/EzeChinedumUchenna/emailApp-GitOps.git"
                        sh "git pull origin HEAD:refs/heads/main emailApp-GitOps"
                        sh "ls -al"
                        sh "ls -al ./emailApp"
                        sh "cat ./emailApp/deployment.yaml"
                        sh "sed -i 's/replaceTag/${BUILD_NUMBER}/g' ./emailApp/deployment.yaml"
                        //sh "cat ./emailApp/deployment.yaml"
                        sh 'git add emailApp/deployment.yaml'
                        sh 'git commit -m "updated deployment.yaml file"'
                        //sh 'git push origin HEAD:refs/heads/main' //here I want to push to main branch. Selete any branch you want to push to Eg sh 'git push origin HEAD:refs/heads/bug-fix'
                        sh 'git push https://${USER}:${PASS}@github.com/EzeChinedumUchenna/emailApp-GitOp HEAD:main'
                       }
                    }
            }
   }    
}
}
