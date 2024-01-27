#!/usr/bin/env groovy

pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://172.210.1.148/:9000'
        SONARQUBE_TOKEN = credentials('OpeEmailAppCredential')
        SONARSCANNER_HOME = tool 'sonarqube-scanner' // Tool name configured in Jenkins Global Tool Configuration
        MAX_ALLOWED_BUGS = 1
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
             waitForQualityGate abortPipeline: true, credentialsId: 'OpeEmailAppCredential'
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
                    // Run Trivy scan on the Docker image
                    def trivyScanOutput = sh(script: 'trivy image --format json --severity HIGH,MEDIUM nedumacr.azurecr.io/nedumpythonapp:$BUILD_NUMBER', returnStdout: true).trim()
                    // Parse Trivy output to check for high-severity vulnerabilities
                    def vulnerabilities = trivyScanOutput.readJSON().Vulnerabilities
                    def highSeverityVulnerabilities = vulnerabilities.findAll { it.Severity == 'HIGH' }

                    // Fail the build or notify stakeholders if high-severity vulnerabilities are found
                    if (highSeverityVulnerabilities) {
                        currentBuild.result = 'FAILURE'
                        error("High-severity vulnerabilities found. Build failed.")
                    } else {
                        echo "No high-severity vulnerabilities found. Build continues."
                    }
                }
            }
        }
}
}
