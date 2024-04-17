pipeline {
    agent any

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

        stage('Static Code Checking') {
            steps {
                script {
                    // Run pylint on Python files and generate a report
                    sh 'find . -name \\*.py | xargs pylint -f parseable | tee pylint.log'
                    recordIssues(
                        tools: [pyLint(pattern: 'pylint.log')],
                        unstableTotalAll: 100
                    )
                }
            }
        }
    }
}
