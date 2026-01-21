pipeline {
    agent any

    stages {
        stage('Clone repo') {
            steps {
                git branch: 'main', url: 'https://github.com/efthimiskalpasidis/yt-transcript-flask.git'
            }
        }

        stage('Deploy with docker compose') {
            steps {
                sh '''
                  docker compose down || true
                  docker compose up -d --build
                '''
            }
        }
    }
}