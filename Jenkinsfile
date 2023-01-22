pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker build --platform linux/arm64 -t $USERNAME/hansung-grade-backend:latest .'
                }
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker login -u $USERNAME -p $PASSWORD'
                    sh 'docker push $USERNAME/hansung-grade-backend:latest'
                }
            }
        }
        stage('Add New Docker Container') {
            steps {
                sh 'docker-compose -f /app/docker-compose.yml up -d'
            }
        }
    }
}