#!groovy

properties([disableConcurrentBuilds()])

pipeline {
    agent any 
    options {
        buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))
        timestamps()
    }
    triggers { pollSCM('* * * * *') }
    stages {
        stage("Build image"){
            steps {
                sh 'docker build -t lyceum-api .'
            }
        }
        stage("Run images"){
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
