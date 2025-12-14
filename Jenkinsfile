pipeline {
    agent any

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Check Python Version') {
            steps {
                sh 'python3 --version || python --version'
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
    }

    post {
        success {
            echo '✅ DevSecOps CI Pipeline executed successfully'
        }
        failure {
            echo '❌ DevSecOps CI Pipeline failed'
        }
    }
}
