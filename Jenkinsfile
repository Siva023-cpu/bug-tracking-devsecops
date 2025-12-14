pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'https://github.com/Siva023-cpu/bug-tracking-devsecops.git'
            }
        }

        stage('Check Python Version') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m venv venv
                venv\\Scripts\\activate
                pip install --upgrade pip
                pip install flask flask_sqlalchemy werkzeug
                '''
            }
        }
    }

    post {
        success {
            echo '✅ CI Pipeline executed successfully'
        }
        failure {
            echo '❌ CI Pipeline failed'
        }
    }
}
