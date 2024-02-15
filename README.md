 Video Link -- https://youtu.be/e42hIYkvxoQ
============================================================= Install and Configure the Jenkins-Master & Jenkins-Agent =============================================================
## Install Java.
$ sudo apt update
$ sudo apt upgrade
$ sudo nano /etc/hostname
$ sudo init 6
$ sudo apt install openjdk-17-jre
$ java -version

## Install Jenkins
Refer--https://www.jenkins.io/doc/book/installing/linux/
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins

$ sudo systemctl enable jenkins       //Enable the Jenkins service to start at boot
$ sudo systemctl start jenkins        //Start Jenkins as a service
$ systemctl status jenkins
$ sudo nano /etc/ssh/sshd_config
$ sudo service sshd reload
$ ssh-keygen OR $ ssh-keygen -t ed25519
$ cd .ssh

============================================================= Install and Configure the SonarQube =============================================================
## Update Package Repository and Upgrade Packages
    $ sudo apt update
    $ sudo apt upgrade
## Add PostgresSQL repository
    $ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    $ wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null
## Install PostgreSQL
    $ sudo apt update
    $ sudo apt-get -y install postgresql postgresql-contrib
    $ sudo systemctl enable postgresql
## Create Database for Sonarqube
    $ sudo passwd postgres
    $ su - postgres
    $ createuser sonar
    $ psql 
    $ ALTER USER sonar WITH ENCRYPTED password 'sonar';
    $ CREATE DATABASE sonarqube OWNER sonar;
    $ grant all privileges on DATABASE sonarqube to sonar;
    $ \q
    $ exit
## Add Adoptium repository
    $ sudo bash
    $ wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc
    $ echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list
 ## Install Java 17
    $ apt update # Or use this if you get error - sudo apt-get update --allow-insecure-repositories 
    $ apt install temurin-17-jdk
    $ update-alternatives --config java
    $ /usr/bin/java --version
    $ exit 
## Linux Kernel Tuning
   # Increase Limits
    $ sudo vim /etc/security/limits.conf
    //Paste the below values at the bottom of the file
    sonarqube   -   nofile   65536
    sonarqube   -   nproc    4096

    # Increase Mapped Memory Regions
    sudo vim /etc/sysctl.conf
    //Paste the below values at the bottom of the file
    vm.max_map_count = 262144
    sudo init 6

#### Sonarqube Installation ####
## Download and Extract
    $ sudo wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.9.0.65466.zip
    $ sudo apt install unzip
    $ sudo unzip sonarqube-9.9.0.65466.zip -d /opt
    $ sudo mv /opt/sonarqube-9.9.0.65466 /opt/sonarqube
## Create user and set permissions
     $ sudo groupadd sonar
     $ sudo useradd -c "user to run SonarQube" -d /opt/sonarqube -g sonar sonar
     $ sudo chown sonar:sonar /opt/sonarqube -R
## Update Sonarqube properties with DB credentials
     $ sudo vim /opt/sonarqube/conf/sonar.properties
     //Find and replace the below values, you might need to add the sonar.jdbc.url
     sonar.jdbc.username=sonar
     sonar.jdbc.password=sonar
     sonar.jdbc.url=jdbc:postgresql://localhost:5432/sonarqube
## Create service for Sonarqube
$ sudo vim /etc/systemd/system/sonar.service
//Paste the below into the file
     [Unit]
     Description=SonarQube service
     After=syslog.target network.target

     [Service]
     Type=forking

     ExecStart=/opt/sonarqube/bin/linux-x86-64/sonar.sh start
     ExecStop=/opt/sonarqube/bin/linux-x86-64/sonar.sh stop

     User=sonar
     Group=sonar
     Restart=always

     LimitNOFILE=65536
     LimitNPROC=4096

     [Install]
     WantedBy=multi-user.target

## Start Sonarqube and Enable service
     $ sudo systemctl start sonar
     $ sudo systemctl enable sonar
     $ sudo systemctl status sonar

## Watch log files and monitor for startup
     $ sudo tail -f /opt/sonarqube/logs/sonar.log

============================================================= Setup Bootstrap Server for eksctl and Setup Kubernetes using eksctl =============================================================
## Install AWS Cli on the above EC2
Refer--https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
$ sudo su
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ apt install unzip,   $ unzip awscliv2.zip
$ sudo ./aws/install
         OR
$ sudo yum remove -y aws-cli
$ pip3 install --user awscli
$ sudo ln -s $HOME/.local/bin/aws /usr/bin/aws
$ aws --version

## Installing kubectl
Refer--https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
$ sudo su
$ curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.27.1/2023-04-19/bin/linux/amd64/kubectl
$ ll , $ chmod +x ./kubectl  //Gave executable permisions
$ mv kubectl /bin   //Because all our executable files are in /bin
$ kubectl version --output=yaml

## Installing  eksctl
Refer---https://github.com/eksctl-io/eksctl/blob/main/README.md#installation
$ curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
$ cd /tmp
$ ll
$ sudo mv /tmp/eksctl /bin
$ eksctl version

## Setup Kubernetes using eksctl
Refer--https://github.com/aws-samples/eks-workshop/issues/734
$ eksctl create cluster --name virtualtechbox-cluster \
--region ap-south-1 \
--node-type t2.small \
--nodes 3 \

$ kubectl get nodes

============================================================= ArgoCD Installation on EKS Cluster and Add EKS Cluster to ArgoCD =============================================================
1 ) First, create a namespace
    $ kubectl create namespace argocd

2 ) Next, let's apply the yaml configuration files for ArgoCd
    $ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

3 ) Now we can view the pods created in the ArgoCD namespace.
    $ kubectl get pods -n argocd

4 ) To interact with the API Server we need to deploy the CLI:
    $ curl --silent --location -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.4.7/argocd-linux-amd64
    $ chmod +x /usr/local/bin/argocd

5 ) Expose argocd-server
    $ kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

6 ) Wait about 2 minutes for the LoadBalancer creation
    $ kubectl get svc -n argocd

7 ) Get pasword and decode it.
    $ kubectl get secret argocd-initial-admin-secret -n argocd -o yaml
    $ echo WXVpLUg2LWxoWjRkSHFmSA== | base64 --decode

## Add EKS Cluster to ArgoCD
9 ) login to ArgoCD from CLI
    $ argocd login <load balancer IP> --username admin

10 ) 
     $ argocd cluster list

11 ) Below command will show the EKS cluster
     $ kubectl config get-contexts

12 ) Add above EKS cluster to ArgoCD with below command
     $ argocd cluster add nedumAKS --name virtualtechbox-nedumAks-cluster
     
     check using below
     $ argocd cluster list

13 ) $ kubectl get svc
============================================================= Cleanup =============================================================
$ kubectl get all
$ kubectl delete deployment.apps/virtualtechbox-regapp       //it will delete the deployment
$ kubectl delete service/virtualtechbox-service              //it will delete the service
$ eksctl delete cluster virtualtechbox --region ap-south-1     OR    eksctl delete cluster --region=ap-south-1 --name=virtualtechbox-cluster      //it will delete the EKS cluster





---TRIVY INSTALLATION STEPS---


sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy


---TRIVY COMMANDS---

trivy image imagename

trivy fs --security-checks vuln,config   Folder_name_OR_Path

trivy image --severity HIGH,CRITICAL image_name

trivy image -f json -o results.json image_name

trivy repo repo-url

trivy k8s --report summary cluster



Video -- https://youtu.be/TY6hW7fecuI
=============================================================================================================================================================================================
[A] Let's use Terraform to create an EC2 instance for Jenkins, Docker and SonarQube
1--main.tf
resource "aws_instance" "web" {
  ami                    = "ami-0287a05f0ef0e9d9a"      #change ami id for different region
  instance_type          = "t2.large"
  key_name               = "Linux-VM-Key7"              #change key name as per your setup
  vpc_security_group_ids = [aws_security_group.Jenkins-VM-SG.id]
  user_data              = templatefile("./install.sh", {})

  tags = {
    Name = "Jenkins-SonarQube"
  }

  root_block_device {
    volume_size = 40
  }
}

resource "aws_security_group" "Jenkins-VM-SG" {
  name        = "Jenkins-VM-SG"
  description = "Allow TLS inbound traffic"

  ingress = [
    for port in [22, 80, 443, 8080, 9000, 3000] : {
      description      = "inbound rules"
      from_port        = port
      to_port          = port
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      security_groups  = []
      self             = false
    }
  ]

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Jenkins-VM-SG"
  }
}


2--provider.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
# Configure the AWS Provider
provider "aws" {
  region = "ap-south-1"     #change region as per you requirement
}


3--install.sh
#!/bin/bash
sudo apt update -y
wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc
echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list
sudo apt update -y
sudo apt install temurin-17-jdk -y
/usr/bin/java --version
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update -y
sudo apt-get install jenkins -y
sudo systemctl start jenkins
sudo systemctl status jenkins

##Install Docker and Run SonarQube as Container
sudo apt-get update
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu
sudo usermod -aG docker jenkins  
newgrp docker
sudo chmod 777 /var/run/docker.sock
docker run -d --name sonar -p 9000:9000 sonarqube:lts-community

#install trivy
sudo apt-get install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy -y

4-- aws configure,  terraform init,  terraform plan,  terraform apply -auto-approve
=============================================================================================================================================================================================
[B] Create EC2 Instance and Setup Prometheus & Grafana
1--main.tf
resource "aws_instance" "web" {
  ami                    = "ami-0287a05f0ef0e9d9a"      #change ami id for different region
  instance_type          = "t2.medium"
  key_name               = "Linux-VM-Key7"              #change key name as per your setup
  vpc_security_group_ids = [aws_security_group.Monitoring-Server-SG.id]
  user_data              = templatefile("./install.sh", {})

  tags = {
    Name = "Monitoring-Server"
  }

  root_block_device {
    volume_size = 20
  }
}

resource "aws_security_group" "Monitoring-Server-SG" {
  name        = "Monitoring-Server-SG"
  description = "Allow TLS inbound traffic"

  ingress = [
    for port in [22, 80, 443, 9090, 9100, 3000] : {
      description      = "inbound rules"
      from_port        = port
      to_port          = port
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      security_groups  = []
      self             = false
    }
  ]

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Monitoring-Server-SG"
  }
}


2--provider.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
# Configure the AWS Provider
provider "aws" {
  region = "ap-south-1"     #change region as per you requirement
}


3--install.sh
#!/bin/bash
sudo apt update -y

##Install Prometheus and Create Service for Prometheus
sudo useradd --system --no-create-home --shell /bin/false prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.47.1/prometheus-2.47.1.linux-amd64.tar.gz
tar -xvf prometheus-2.47.1.linux-amd64.tar.gz
cd prometheus-2.47.1.linux-amd64/
sudo mkdir -p /data /etc/prometheus
sudo mv prometheus promtool /usr/local/bin/
sudo mv consoles/ console_libraries/ /etc/prometheus/
sudo mv prometheus.yml /etc/prometheus/prometheus.yml
sudo chown -R prometheus:prometheus /etc/prometheus/ /data/
sudo cat > /etc/systemd/system/prometheus.service << EOF
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/data \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --web.listen-address=0.0.0.0:9090 \
  --web.enable-lifecycle

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable prometheus
sudo systemctl start prometheus

##Install Node Exporter and Create Service for Node Exporter
sudo useradd --system --no-create-home --shell /bin/false node_exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar -xvf node_exporter-1.6.1.linux-amd64.tar.gz
sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
rm -rf node_exporter*
sudo cat > /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
User=node_exporter
Group=node_exporter
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/node_exporter --collector.logind

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

##Install Grafana
$ sudo apt-get update
$ sudo apt-get install -y apt-transport-https software-properties-common
$ wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
$ echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
$ sudo apt-get update
$ sudo apt-get -y install grafana
$ sudo systemctl enable grafana-server
$ sudo systemctl start grafana-server


4--Commands to check services
$ sudo systemctl status prometheus
$ sudo systemctl status node_exporter
$ sudo systemctl status grafana-server

5--Add job for node exporter in prometheus
$ cd /etc/prometheus/, ls, $ sudo nano prometheus.yml and below the job of prometheus, add job for node exporter
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['IP-Address:9100']

6--Check the indentatio of the prometheus config file with below command
$ promtool check config /etc/prometheus/prometheus.yml

7--Reload the Prometheus configuration
$ curl -X POST http://localhost:9090/-/reload

8--On monitoring server go to $ cd /etc/prometheus/ & $ sudo nano prometheus.yml and add job for Jenkins
- job_name: 'jenkins'
    metrics_path: '/prometheus'
    static_configs:
      - targets: ['IP-Address:8080']
=============================================================================================================================================================================================
[C] Create AWS EKS Cluster
1--Install kubectl on Jenkins Server
 $ sudo apt update
 $ sudo apt install curl
 $ curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
 $ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
 $ kubectl version --client

2--Install AWS Cli
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ sudo apt install unzip
$ unzip awscliv2.zip
$ sudo ./aws/install
$ aws --version

3--Installing  eksctl
$ curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
$ cd /tmp
$ sudo mv /tmp/eksctl /bin
$ eksctl version

4--Setup Kubernetes using eksctl
eksctl create cluster --name virtualtechbox-cluster \
--region ap-south-1 \
--node-type t2.small \
--nodes 3 \

5--Verify Cluster with below command
$ kubectl get nodes
=============================================================================================================================================================================================
[D] Integrate Prometheus with EKS and Import Grafana Monitoring Dashboard for Kubernetes
1--Install Helm
$ sudo snap install helm --classic,    $ helm version
                    OR
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
$ helm version


2--Install Prometheus on EKS
$ helm repo add stable https://charts.helm.sh/stable          ///We need to add the Helm Stable Charts for our local client

$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts     ///Add Prometheus Helm repo

$ kubectl create namespace prometheus            ///Create Prometheus namespace

$ helm install stable prometheus-community/kube-prometheus-stack -n prometheus      ///Install Prometheus

$ kubectl get pods -n prometheus          ///To check whether Prometheus is installed

$ kubectl get svc -n prometheus           ///to check the services file (svc) of the Prometheus


##let’s expose Prometheus to the external world using LoadBalancer
$ kubectl edit svc stable-kube-prometheus-sta-prometheus -n prometheus    ///type:LoadBalancer, change port & targetport to 9090, save and close

$ kubectl get svc -n prometheus    //copy dns name of LB and browse with 9090
=============================================================================================================================================================================================
[E] Set the Trigger and Verify the CI/CD Pipeline
$ git config --global user.name "your.name"
$ git config --global user.email "your-email-address"
$ git clone https://github.com/Ashfaque-9x/a-youtube-clone-app.git
$ cd a-youtube-clone-app
$ git add .
$ git commit -m "test change"
$ git push origin main
=============================================================================================================================================================================================
[F] Complete jenkins pipeline script
pipeline {
    agent any
    tools {
        jdk 'jdk17'
        nodejs 'node16'
    }
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
    }
    stages {
        stage('clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout from Git') {
            steps {
                git branch: 'main', url: 'https://github.com/Ashfaque-9x/a-youtube-clone-app.git'
            }
        }
        stage("Sonarqube Analysis") {
            steps {
                withSonarQubeEnv('SonarQube-Server') {
                    sh '''$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=Youtube-CICD \
                    -Dsonar.projectKey=Youtube-CICD'''
                }
            }
        }
        stage("Quality Gate") {
            steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'SonarQube-Token'
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                sh "npm install"
            }
        }
        stage('TRIVY FS SCAN') {
             steps {
                 sh "trivy fs . > trivyfs.txt"
             }
         }
         stage("Docker Build & Push"){
             steps{
                 script{
                   withDockerRegistry(credentialsId: 'dockerhub', toolName: 'docker'){   
                      sh "docker build -t youtube-clone ."
                      sh "docker tag youtube-clone ashfaque9x/youtube-clone:latest "
                      sh "docker push ashfaque9x/youtube-clone:latest "
                    }
                }
            }
        }
        stage("TRIVY Image Scan"){
            steps{
                sh "trivy image ashfaque9x/youtube-clone:latest > trivyimage.txt" 
            }
        }
        stage('Deploy to Kubernets'){
            steps{
                script{
                    dir('Kubernetes') {
                      withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'kubernetes', namespace: '', restrictKubeConfigAccess: false, serverUrl: '') {
                      sh 'kubectl delete --all pods'
                      sh 'kubectl apply -f deployment.yml'
                      sh 'kubectl apply -f service.yml'
                      }   
                    }
                }
            }
        }
    }
    post {
     always {
        emailext attachLog: true,
            subject: "'${currentBuild.result}'",
            body: "Project: ${env.JOB_NAME}<br/>" +
                "Build Number: ${env.BUILD_NUMBER}<br/>" +
                "URL: ${env.BUILD_URL}<br/>",
            to: 'ashfaque.s510@gmail.com',                              
            attachmentsPattern: 'trivyfs.txt,trivyimage.txt'
        }
    }
}

=============================================================================================================================================================================================
[G] Cleanup
$ kubectl delete --all pods -n prometheus                   //This command will delete all the pods in prometheus namespace
$ kubectl delete namespace prometheus
$ kubectl get all                                           //This command will show the all the deployments, pods & services in default namespace
$ kubectl delete deployment.apps/virtualtechbox-cluster     //delete deployment in your k8s cluster
$ kubectl delete service/virtualtechbox-service             //delete service for your deployment of k8s cluster
$ eksctl delete cluster virtualtechbox-cluster --region ap-south-1     OR    eksctl delete cluster --region=ap-south-1 --name=virtualtechbox-cluster      //This command will delete your EKS cluster
$ terraform destroy
