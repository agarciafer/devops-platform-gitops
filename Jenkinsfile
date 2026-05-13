pipeline {

    agent {
        label 'principal'
    }

    parameters {

        string(
            name: 'VERSION',
            defaultValue: 'v1',
            description: 'Version de la imagen Docker'
        )

        string(
            name: 'REPLICAS',
            defaultValue: '2',
            description: 'Numero de replicas Kubernetes'
        )
    }

    environment {

        DOCKER_IMAGE = "agarciafer/devops-platform:${VERSION}"

        GIT_REPO = "https://github.com/agarciafer/devops-platform-gitops.git"

        GITOPS_FILE = "gitops/app/deployment.yaml"
    }

    stages {

        stage('Clone Repository') {

            steps {

                git branch: 'main',
                credentialsId: 'github-token',
                url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {

            steps {

                sh '''
                    cd app

                    docker build -t ${DOCKER_IMAGE} .
                '''
            }
        }

        stage('Push DockerHub') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin

                        docker push ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('Update GitOps Deployment') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {

                    sh '''
                        git fetch origin main

                        git checkout -B main origin/main

                        sed -i "s|image: agarciafer/devops-platform:.*|image: agarciafer/devops-platform:${VERSION}|g" ${GITOPS_FILE}

                        sed -i "s|replicas: .*|replicas: ${REPLICAS}|g" ${GITOPS_FILE}

                        git config user.email "jenkins@local"

                        git config user.name "jenkins"

                        git add ${GITOPS_FILE}

                        git commit -m "Update image ${VERSION} and replicas ${REPLICAS}" || echo "No hay cambios"

                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/agarciafer/devops-platform-gitops.git HEAD:main
                    '''
                }
            }
        }
    }

    post {

        success {

            echo 'Pipeline GitOps completado correctamente'
        }

        failure {

            echo 'Pipeline GitOps fallido'
        }
    }
}
