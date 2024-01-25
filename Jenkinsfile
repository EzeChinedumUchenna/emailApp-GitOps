#!/usr/bin/env groovy

pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://172.210.1.148/:9000'
        SONARQUBE_TOKEN = credentials('OpeEmailAppCredential')
        SONARSCANNER_HOME = tool 'sonarqube-scanner' // Tool name configured in Jenkins Global Tool Configuration
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
                        sh 'docker build -t nedumpythonapp:$BUILD_NUMBER .'
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
    } 
}
