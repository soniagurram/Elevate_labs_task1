pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = credentials('dockerhub-username') // Jenkins secret
        DOCKERHUB_PASSWORD = credentials('dockerhub-password') // Jenkins secret
        KUBE_CONFIG_BASE64 = credentials('kubeconfig-base64')  // Jenkins secret
        PYTHONPATH = "${env.WORKSPACE}"
        GITHUB_REPO_URL = 'https://github.com/soniagurram/Elevate_labs_task1.git'
    }

    stages {

        stage('Checkout') {
            steps {
                powershell """
                    # Clean workspace
                    if (Test-Path .git) { Remove-Item -Recurse -Force .git }
                    git clone ${env.GITHUB_REPO_URL} .
                """
            }
        }

        stage('Test') {
            agent { label 'windows' }
            steps {
                powershell '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            agent { label 'windows' }
            steps {
                powershell '''
                    docker build -t ${env.DOCKERHUB_USERNAME}/fastapi-app:latest .
                    docker save ${env.DOCKERHUB_USERNAME}/fastapi-app:latest -o fastapi-app.tar
                '''
                archiveArtifacts artifacts: 'fastapi-app.tar', fingerprint: true
            }
        }

        stage('Push Docker Image') {
            agent { label 'windows' }
            steps {
                powershell '''
                    docker load -i fastapi-app.tar
                    docker login -u ${env.DOCKERHUB_USERNAME} -p ${env.DOCKERHUB_PASSWORD}
                    docker push ${env.DOCKERHUB_USERNAME}/fastapi-app:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            agent { label 'windows' }
            steps {
                powershell '''
                    if (-Not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
                        Invoke-WebRequest -Uri https://dl.k8s.io/release/v1.30.0/bin/windows/amd64/kubectl.exe -OutFile kubectl.exe
                        $env:PATH += ";$PWD"
                    }

                    [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("${env.KUBE_CONFIG_BASE64}")) | Out-File kubeconfig
                    $env:KUBECONFIG = "$PWD\\kubeconfig"

                    kubectl apply -f k8s\\deployment.yaml
                    kubectl rollout status deployment/fastapi-app --timeout=120s
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
