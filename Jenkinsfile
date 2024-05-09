pipeline{
    agent any
    stages{
        stage('Checkout'){
            steps{
            checkout scmGit(branches: [[name: '*/done']], extensions: [], userRemoteConfigs: [[credentialsId: '8d399890-9945-4ab3-a08e-36782fd085ee', url: 'https://github.com/dristi-sigdel/soaltee_bot']])            }
        }
        stage('Copy env files'){
            steps{
                sh '''
                  sudo cp /home/sagar/rasa-envs/.sql.env .
                  sudo cp /home/sagar/rasa-envs/.env flask
                '''
            }
        }
        stage('Build'){
            steps{
                sh '''
                sudo docker-compose up -d --build
                '''
            }
        }
    }
}

