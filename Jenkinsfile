pipeline {
    agent any
    environment {
        DOCKER_USERNAME = credentials('docker-hub').username
        DOCKER_PASSWORD = credentials('docker-hub').password
        DOCKER_IMAGE_NAME = '${env.JOB_NAME}'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$BUILD_NUMBER .'
            }
        }
        stage('Push Image') {
            steps {
                sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                sh 'docker push $DOCKER_USERNAME/$DOCKER_IMAGE_NAME:$BUILD_NUMBER'
            }
        }
        stage('Add New Docker Container') {
            steps {
                sh 'cd /app && docker-compose up -d --build'
            }
        }
    }
}