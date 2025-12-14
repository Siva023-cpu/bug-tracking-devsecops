pipeline {
    agent any

    environment {
        IMAGE_NAME = "bugtracker-devsecops"
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Check Python Version') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality Check (Flake8)') {
            steps {
                sh '''
                . venv/bin/activate
                flake8 app.py models.py || true
                '''
            }
        }

        stage('Static Security Scan (Bandit)') {
            steps {
                sh '''
                . venv/bin/activate
                bandit -r app.py models.py || true
                '''
            }
        }

        stage('Dependency Vulnerability Scan') {
            steps {
                sh '''
                . venv/bin/activate
                pip-audit || true
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Docker Run (Test Container)') {
            steps {
                sh '''
                docker stop bugtracker || true
                docker rm bugtracker || true
                docker run -d -p 5000:5000 --name bugtracker $IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo "✅ DevSecOps CI/CD with Docker completed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
