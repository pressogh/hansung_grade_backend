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
                    sh 'docker build --platform linux/arm64 -t $USERNAME/$JOB_NAME:latest .'
                }
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker login -u $USERNAME --password-stdin $PASSWORD'
                    sh 'docker push $USERNAME/$JOB_NAME:latest'
                }
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker login -u $USERNAME --password-stdin $PASSWORD'
                    sh 'docker pull $USERNAME/$JOB_NAME:latest'
                    sh 'docker container update --restart unless-stopped $USERNAME/$JOB_NAME'
                }
            }
        }
    }
}