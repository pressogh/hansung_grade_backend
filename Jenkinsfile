node {
    stage('Checkout') {
        checkout scm
    }
    stage('Build Docker Image') {
        sh 'docker build -t hansung-grade-backend .'
    }
    stage('Push Docker Image') {
        withCredentials([usernamePassword(credentials
        id: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
            sh 'docker login -u $USERNAME -p $PASSWORD'
            sh 'docker tag hansung-grade-backend $USERNAME/hansung-grade-backend'
            sh 'docker push $USERNAME/hansung-grade-backend'
        }
    }
    stage('Add New Docker Container') {
        sh 'cd /app && docker-compose up -d --build'
    }
}