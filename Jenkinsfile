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
        stage('Clean Up') {
            steps {
                script {
                    
                    // Stop and remove all containers except for SonarQube, Python, and the specified container ID
                    sh 'docker ps -a --format "{{.ID}} {{.Names}}" | grep -v "1d4ffdefc3bc\|sonarqube:lts-community\|python" | awk \'{print $1}\' | xargs -r docker stop'
                    sh 'docker ps -a --format "{{.ID}} {{.Names}}" | grep -v "1d4ffdefc3bc\|sonarqube:lts-community\|python" | awk \'{print $1}\' | xargs -r docker rm -f'
                    
                    
                    // Remove all images except for SonarQube and Python
                    sh 'docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "sonarqube:lts-community\|python" | xargs -r docker rmi -f'

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

        stage(' Push image to ECR Repository') {
            steps {
                script {

                    sh '''
                    aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/t1m3i4h4
                    docker push public.ecr.aws/t1m3i4h4/monitoring-app:latest
                    '''
                }
            }
        }
}
}


