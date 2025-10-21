pipeline {
    agent any

    environment {
        // Replace these with the IDs of the credentials you added in Jenkins
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials-id'
        KUBECONFIG_SECRET = 'kubeconfig-base64'
        GITHUB_REPO = 'https://github.com/soniagurram/Elevate_labs_task1.git'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs() // Remove any old files in the workspace
            }
        }

        stage('Checkout') {
            steps {
                git url: "${GITHUB_REPO}", branch: 'main'
            }
        }

        stage('Test') {
            agent { label 'windows' }  // or ubuntu if you prefer
            steps {
                powershell '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    $env:PYTHONPATH="$env:PYTHONPATH;${pwd()}"
                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            agent { label 'windows' } // or ubuntu
            steps {
                powershell '''
                    docker build -t soniagurram/fastapi-app:latest .
                    docker save soniagurram/fastapi-app:latest -o fastapi-app.tar
                '''
                // Optionally archive image as artifact
                archiveArtifacts artifacts: 'fastapi-app.tar', fingerprint: true
            }
        }

        stage('Push Docker Image') {
            agent { label 'windows' } // or ubuntu
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", 
                                                  usernameVariable: 'DOCKER_USER', 
                                                  passwordVariable: 'DOCKER_PASSWORD')]) {
                    powershell '''
                        docker load -i fastapi-app.tar
                        docker login -u $env:DOCKER_USER -p $env:DOCKER_PASSWORD
                        docker push soniagurram/fastapi-app:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            agent { label 'windows' } // the agent must have kubectl installed
            steps {
                withCredentials([string(credentialsId: "${KUBECONFIG_SECRET}", variable: 'KUBE_CONFIG_BASE64')]) {
                    powershell '''
                        # Decode kubeconfig
                        [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($env:KUBE_CONFIG_BASE64)) | Out-File kubeconfig
                        $env:KUBECONFIG="$PWD\\kubeconfig"

                        # Apply Kubernetes manifests
                        kubectl apply -f deployment.yaml

                        # Verify rollout
                        kubectl rollout status deployment/fastapi-app --timeout=120s

                        # Show service info
                        kubectl get svc fastapi-app-service -o wide
                    '''
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
