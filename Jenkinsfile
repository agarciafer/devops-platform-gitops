pipeline { // Inicio del pipeline declarativo de Jenkins

    agent { // Define dónde se ejecutará el pipeline
        label 'principal' // Ejecuta el pipeline en el nodo Jenkins con la etiqueta 'principal'
    }

    parameters { // Define parámetros que Jenkins pedirá antes de ejecutar el job

        string(
            name: 'VERSION', // Nombre del parámetro
            defaultValue: 'v1', // Valor por defecto
            description: 'Version de la imagen Docker' // Descripción que verá el usuario
        )

        string(
            name: 'REPLICAS', // Nombre del parámetro
            defaultValue: '2', // Número de réplicas por defecto
            description: 'Numero de replicas Kubernetes' // Descripción del parámetro
        )
    }

    environment { // Variables globales del pipeline
        DOCKER_IMAGE = "agarciafer/devops-platform:${VERSION}" // Nombre completo de la imagen Docker
        GIT_REPO = "https://github.com/agarciafer/devops-platform-gitops.git" // Repositorio GitHub
        GITOPS_FILE = "gitops/app/deployment.yaml" // Fichero Kubernetes que se modificará
    }

    stages { // Bloque principal de fases del pipeline

        stage('Clone Repository') { // Fase 1: clonar repositorio
            steps {
                git branch: 'main', // Clona la rama main
                    credentialsId: 'github-token', // Usa credenciales GitHub guardadas en Jenkins
                    url: "${GIT_REPO}" // URL del repositorio
            }
        }

        stage('Build Docker Image') { // Fase 2: construir imagen Docker
            steps {
                sh '''
                    cd app
                    docker build -t ${DOCKER_IMAGE} .
                '''
                // Entra en la carpeta app y construye la imagen Docker
            }
        }

        stage('Push DockerHub') { // Fase 3: subir imagen a DockerHub
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'agarciafer-dockerhub', // Credencial DockerHub en Jenkins
                        usernameVariable: 'DOCKER_USER', // Variable con el usuario DockerHub
                        passwordVariable: 'DOCKER_PASS' // Variable con el token/password DockerHub
                    )
                ]) {
                    sh '''
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${DOCKER_IMAGE}
                    '''
                    // Hace login seguro en DockerHub y sube la imagen
                }
            }
        }

        stage('Update GitOps Deployment') { // Fase 4: modificar deployment.yaml
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token', // Credencial GitHub en Jenkins
                        usernameVariable: 'GIT_USER', // Usuario GitHub
                        passwordVariable: 'GIT_TOKEN' // Token GitHub
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
                    // Actualiza imagen y réplicas, hace commit y push a GitHub
                }
            }
        }
    }

    post { // Acciones finales del pipeline

        success { // Si todo termina correctamente
            echo 'Pipeline GitOps completado correctamente'
        }

        failure { // Si alguna fase falla
            echo 'Pipeline GitOps fallido'
        }
    }
}
