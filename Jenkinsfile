#!/usr/bin/env groovy

pipeline {
    agent any
 
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

        stage('Build') {
            steps {
                script {
                    // Install dependencies and run tests
                    sh 'pip install -r requirements.txt'
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
        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonarqube-server') {
                        sh 'sonar-scanner'
                    }
                }
            }
        }
    } 
}
