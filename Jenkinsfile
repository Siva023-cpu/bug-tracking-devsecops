pipeline {
    agent any

    environment {
        IMAGE_NAME = "vasgrills/bugtracker-webapp"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        LATEST_TAG = "latest"
        CONTAINER_NAME = "bugtracker"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
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

        stage('Setup Virtual Environment & Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Auto Format Code') {
            steps {
                sh '''
                . venv/bin/activate
                pip install autopep8
                autopep8 --in-place --recursive app
                '''
            }
        }


        stage('Code Quality Check (Flake8)') {
            steps {
                sh '''
                . venv/bin/activate
                flake8 app || true
                '''
            }
        }

        stage('Static Security Scan (Bandit)') {
            steps {
                sh '''
                . venv/bin/activate
                bandit -r app || true
                '''
            }
        }

        stage('Dependency Vulnerability Scan') {
            steps {
                sh '''
                . venv/bin/activate
                pip install pip-audit
                pip-audit
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:$LATEST_TAG
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                docker stop bugtracker || true
                docker rm bugtracker || true

                docker run -d \
                --network jenkins-net \
                --name bugtracker \
                $IMAGE_NAME:$IMAGE_TAG

                sleep 5

                curl -f http://bugtracker:5000 || exit 1
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
                docker push $IMAGE_NAME:$LATEST_TAG
                '''
            }
        }
    }

    post {
        success {
            echo "✅ DevSecOps Pipeline SUCCESS"
        }
        failure {
            echo "❌ Pipeline FAILED"
        }
        always {
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            docker logout || true
            '''
            cleanWs()
        }
    }
}
