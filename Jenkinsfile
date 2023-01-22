node {
    stage('Checkout') {
        checkout scm
    }
    stage('Build Image') {
        app = docker.build("pressodh/hansung-grade-backend", "--platform linux/amd64 .")
    }
    stage('Push Image') {
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
    stage('Add New Docker Container') {
        sh 'cd /app && docker-compose up -d --build'
    }
}