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
                    sh 'docker build --platform linux/amd64,linux/arm64,linux/arm/v7 -t $USERNAME/${env.JOB_NAME}:$BUILD_NUMBER .'
                }
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker login -u $USERNAME -p $PASSWORD'
                    sh 'docker push $USERNAME/${env.JOB_NAME}:$BUILD_NUMBER'
                }
            }
        }
        stage('Add New Docker Container') {
            steps {
                sh 'cd /app && docker-compose up -d --build'
            }
        }
    }
}