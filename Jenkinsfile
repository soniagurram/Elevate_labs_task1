pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
        KUBECONFIG_SECRET = 'kubeconfig-base64'
        GITHUB_REPO = 'https://github.com/soniagurram/Elevate_labs_task1.git'
        PYTHON_HOME = 'C:\\Users\\sonia\\AppData\\Local\\Programs\\Python\\Python312'
        PATH = "${env.PYTHON_HOME};${env.PYTHON_HOME}\\Scripts;${env.PATH}"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                git url: "${GITHUB_REPO}", branch: 'main'
            }
        }

        stage('Test') {
            steps {
                bat """
                    python --version
                    pip --version
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    set PYTHONPATH=%PYTHONPATH%;%cd%
                    pytest
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                    docker build -t soniagurram/fastapi-app:v1 .
                    docker save soniagurram/fastapi-app:v1 -o fastapi-app.tar
                """
                archiveArtifacts artifacts: 'fastapi-app.tar', fingerprint: true
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", 
                                                  usernameVariable: 'DOCKER_USER', 
                                                  passwordVariable: 'DOCKER_PASSWORD')]) {
                    bat """
                        docker load -i fastapi-app.tar
                        docker login -u %DOCKER_USER% -p %DOCKER_PASSWORD%
                        docker push soniagurram/fastapi-app:v1
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([string(credentialsId: "${KUBECONFIG_SECRET}", variable: 'KUBE_CONFIG_BASE64')]) {
                    bat """
                        powershell -Command "[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('%KUBE_CONFIG_BASE64%')) | Out-File kubeconfig -Encoding UTF8"
                        set KUBECONFIG=%cd%\\kubeconfig
                        kubectl apply -f deployment.yaml
                        kubectl rollout status deployment/fastapi-app --timeout=120s
                        kubectl get svc fastapi-app-service -o wide
                    """
                }
            }
        }

    }

    post {
        always {
            cleanWs()
        }
    }
}
