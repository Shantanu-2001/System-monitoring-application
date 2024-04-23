pipeline {
    agent any

    environment {
        SCANNER_HOME=tool 'sonar-scanner'
      }
    stages {
        stage('Checkout') {
            steps {
               git branch: 'main', url: 'https://github.com/Shantanu-2001/System-monitoring-application.git'
            }
        }
        stage('Installing packages') {
            steps {
                script {
                    // Install required python packages
                    sh 'pip install -r requirements.txt'
                    
                }
            }
        }
        stage("Sonarqube Analysis "){
            steps{
                withSonarQubeEnv('sonar-server') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=Monitoring-app \
                    -Dsonar.projectKey=Monitoring-app '''
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script{
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token'
            }
        }
       }
        stage('TRIVY FS SCAN') {
            steps {
                sh "trivy fs . > trivyfs.txt"
            }
        }
        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('Docker build and Push') {
            steps {
                script{
                    withDockerRegistry(credentialsId: 'docker', toolName: 'docker') {
                        sh '''
                        docker build -t monitoring-app .
                        docker tag monitoring-app shantanu2001/monitoring-app:latest
                        docker run -d -p 5000:5000 monitoring-app:latest
                        docker push shantanu2001/monitoring-app:latest
                        '''
                    }
            }
        } 
    }
        stage('Docker Image Scan') {
            steps {
                sh 'trivy image shantanu2001/monitoring-app:latest > trivyimage.txt'
            }
        }

        stage('Create ECR Repository') {
            steps {
                script {
                    // Create ECR repository if it doesn't exist
                    sh "aws ecr describe-repositories --repository-names ${AWS_ECR_REPO} || aws ecr create-repository --repository-name ${AWS_ECR_REPO}"
                }
            }
        }
}
}


