# Movie Picture Pipeline

An automated continuous integration and continuous deployment (CI/CD) pipeline built with GitHub Actions, Docker, and Kubernetes (AWS EKS) for a microservices-based Movie Picture web application.

---

## 🌐 Live Microservice URLs

The application is deployed to an AWS EKS cluster with LoadBalancer services:

* **Frontend Web UI:** [http://a924ebd0312904a1b822a137938daa23-421438864.us-east-1.elb.amazonaws.com](http://a924ebd0312904a1b822a137938daa23-421438864.us-east-1.elb.amazonaws.com)
* **Backend REST API:** [http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com/movies](http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com/movies)
* **GitHub Repository:** [https://github.com/githubtanush/movie-picture-pipeline](https://github.com/githubtanush/movie-picture-pipeline)

---

## 🏗️ Architecture Overview

* **Frontend Application (`starter/frontend`):** React 18 & TypeScript Single Page Application served using production-ready Node/Express.
* **Backend Application (`starter/backend`):** Python 3.10 Flask REST API served using uWSGI with full CORS enablement.
* **Orchestration & Infrastructure:** Provisioned with Terraform on AWS EKS using Kustomize for continuous deployment.
* **CI/CD Automation:** GitHub Actions with parallel linting, automated testing, container builds, and zero-downtime rolling updates.

---

## 🚀 CI/CD Pipeline Implementation

### 1. Frontend Workflows
* **`frontend-ci.yaml` (Pull Requests & Manual Dispatch):**
  * **lint:** Runs `npm run lint` with ESLint.
  * **test:** Executes Jest unit tests in non-interactive mode (`npm test -- --watchAll=false`).
  * **build:** Runs after `lint` and `test` pass, verifying the production bundle compiles (`npm run build`).
* **`frontend-cd.yaml` (Push to Main Branch & Manual Dispatch):**
  * Runs linting, testing, and Docker image builds.
  * Dynamically injects `REACT_APP_MOVIE_API_URL` via GitHub Repository Secrets through `--build-arg`.
  * Pushes the image to Amazon ECR tagged with the Git commit SHA and `latest`.
  * Deploys the container using `kustomize edit set image` and rolls out the update on AWS EKS.

### 2. Backend Workflows
* **`backend-ci.yaml` (Pull Requests & Manual Dispatch):**
  * **lint:** Runs `flake8` standards against all Python source files.
  * **test:** Runs `pytest` test suites verifying JSON structure and HTTP 200 responses.
* **`backend-cd.yaml` (Push to Main Branch & Manual Dispatch):**
  * Executes linting and automated testing.
  * Builds the uWSGI Python container image and pushes it to Amazon ECR.
  * Dynamically updates the deployment manifest via Kustomize and performs a rolling release to AWS EKS.

---

## 🔐 Required GitHub Repository Secrets

Configure these under **Settings > Secrets and variables > Actions**:

| Secret Name | Description / Example |
| :--- | :--- |
| `AWS_ACCESS_KEY_ID` | Temporary or IAM User AWS Access Key |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Access Key |
| `AWS_SESSION_TOKEN` | AWS Session Token (for Learner Lab/Gateway sessions) |
| `AWS_DEFAULT_REGION` | AWS Deployment Region (e.g., `us-east-1`) |
| `EKS_CLUSTER_NAME` | Name of the provisioned EKS cluster |
| `FRONTEND_ECR_REPO` | ECR repository name for the Frontend app |
| `BACKEND_ECR_REPO` | ECR repository name for the Backend app |
| `REACT_APP_MOVIE_API_URL` | `http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com` |

---

## 💻 Local Development & Testing

### Frontend
```bash
cd starter/frontend

# Install dependencies
npm ci

# Run linter and tests
npm run lint
npm test -- --watchAll=false

# Start development server
REACT_APP_MOVIE_API_URL=http://localhost:5000 npm start
cd starter/backend

# Install dependencies
pipenv install

# Run linter and unit tests
pipenv run lint
pipenv run test

# Run application locally
pipenv run serve
kubectl get pods -l app=backend
kubectl get pods -l app=frontend
kubectl get svc
curl -i [http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com/movies](http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com/movies)
HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *

{"movies":[{"id":"123","title":"Top Gun: Maverick"},{"id":"456","title":"Sonic the Hedgehog"},{"id":"789","title":"A Quiet Place"}]}
