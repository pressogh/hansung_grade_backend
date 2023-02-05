pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Set environment values from Jenkins') {
			steps {
				withCredentials([file(credentialsId: 'hansung-grade-backend-env', variable: 'FILE')]) {
				    sh 'cp $FILE .env'
				}
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
                    sh 'docker login -u $USERNAME -p $PASSWORD'
                    sh 'docker push $USERNAME/$JOB_NAME:latest'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh 'docker pull $USERNAME/$JOB_NAME:latest'
                        try {
                            sh 'docker stop $JOB_NAME'
                            sh 'docker rm $JOB_NAME'
                        } catch (Exception e) {
                            echo 'Container not found'
                        }
                        sh 'docker run -d \
                            --name $JOB_NAME \
                            --restart unless-stopped \
                            -v /tmp:/tmp \
                            -e "TZ=Asia/Seoul" \
                            $USERNAME/$JOB_NAME:latest'
                    }
                }
            }
        }
        stage ('Publish Results') {
            steps{
                script{
                    echo "End"
                    slackSend color: "good", message: "WSGI Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` \n<${env.BUILD_URL}|Open in Jenkins>"
                }
            }
        }
    }
}