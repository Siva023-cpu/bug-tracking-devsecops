pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasgrills/bugtracker-webapp"
        IMAGE_TAG  = "latest"
        CONTAINER_NAME = "bugtracker"
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
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Docker Run (Test Container)') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }

    post {
        success {
            echo "✅ DevSecOps CI/CD completed & Docker image pushed to Docker Hub"
        }
        failure {
            echo "❌ Pipeline failed"
        }
        always {
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            '''
        }
    }
}
