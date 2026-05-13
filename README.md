# DevOps Platform Cloud 

## 📌 Descripción

Proyecto práctico enfocado en la construcción de una plataforma cloud-native utilizando Kubernetes, GitOps y automatización de despliegues.

La primera etapa del proyecto se centró en construir una base sólida de infraestructura y despliegue declarativo utilizando Docker, Kubernetes y ArgoCD.

---

# 🚀 Objetivos de la Etapa 1

- Containerizar una aplicación Flask
- Implementar un clúster Kubernetes local con k3d/k3s
- Desplegar aplicaciones mediante Deployments y Services
- Implementar GitOps con ArgoCD
- Automatizar despliegues mediante sincronización con GitHub
- Realizar rolling updates sin downtime
- Comprender Desired State y Self-Healing

---

# 🏗️ Arquitectura

```text
GitHub
   ↓
ArgoCD
   ↓
Kubernetes Cluster (k3d/k3s)
   ↓
Deployment
   ↓
Pods
   ↓
Service (NodePort)
```

---

# 🧰 Tecnologías utilizadas

- Python / Flask
- Docker
- Docker Hub
- Kubernetes
- k3d / k3s
- ArgoCD
- GitHub
- GitOps

---

# 📂 Estructura del proyecto

```text
.
├── app
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates
│
├── gitops
│   ├── app
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   │
│   └── argocd
│       └── application.yaml
│
├── k8s
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── namespace.yaml
│
├── monitoring
├── logging
├── diagrams
└── screenshots
```

---

# 🐳 Docker

## Construcción de imagen

```bash
docker build -t agarciafer/devops-platform:v1 .
```

## Push a Docker Hub

```bash
docker push agarciafer/devops-platform:v1
```

---

# ☸️ Kubernetes

## Crear namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

## Deployment

La aplicación fue desplegada utilizando:

- múltiples réplicas
- rolling updates
- variables de entorno
- imágenes versionadas

## Service

Se utilizó un Service tipo NodePort para exponer la aplicación:

```yaml
type: NodePort
```

---

# 🔄 GitOps con ArgoCD

Se configuró ArgoCD para sincronizar automáticamente el estado del clúster con el repositorio GitHub.

## Flujo GitOps

```text
Git Push
   ↓
ArgoCD detecta cambios
   ↓
Kubernetes aplica nuevo estado
   ↓
Rolling Update automático
```

---

# 🔥 Rolling Update — v1 → v2

Durante la etapa se realizó una actualización completa de la aplicación:

- Construcción de nueva imagen Docker (`v2`)
- Push a Docker Hub
- Actualización declarativa del Deployment
- Sincronización automática mediante ArgoCD
- Reemplazo progresivo de Pods sin downtime

---

# ✅ Resultados obtenidos

- Aplicación containerizada y desplegada
- Cluster Kubernetes funcional
- GitOps operativo
- Despliegues automatizados
- Self-Healing habilitado
- Rolling Updates exitosos
- Arquitectura declarativa funcionando

---

# 📌 Próxima etapa

La Etapa 2 incluirá:

- Ingress + Traefik
- Prometheus
- Grafana
- Loki
- Promtail
- Observabilidad completa
- CI/CD con GitHub Actions

---

# 👨‍💻 Autor
Alberto Garcia

## 🔗 Repositorio
https://github.com/agarciafer/devops-platform-gitops.git
