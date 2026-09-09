# Movie Picture Pipeline

An automated continuous integration and continuous deployment (CI/CD) pipeline built with GitHub Actions, Docker, Amazon ECR, and Kubernetes (AWS EKS) for a microservices-based Movie Picture web application.

---

## 🌐 Live Microservice Endpoints

The microservices are continuously deployed to an AWS EKS cluster via AWS Elastic Load Balancers:

* **Frontend Web Application:** [http://a924ebd0312904a1b822a137938daa23-421438864.us-east-1.elb.amazonaws.com](http://a924ebd0312904a1b822a137938daa23-421438864.us-east-1.elb.amazonaws.com)
* **Backend REST API (`/movies`):** [http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com/movies](http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com/movies)
* **Source Repository:** [https://github.com/githubtanush/movie-picture-pipeline](https://github.com/githubtanush/movie-picture-pipeline)

---

## 🏗️ Architecture & Tech Stack

* **Frontend Application (`starter/frontend`):** React 18 and TypeScript Single Page Application served via a production Node/Express runtime.
* **Backend REST API (`starter/backend`):** Python 3.10 Flask service served using uWSGI with enabled Cross-Origin Resource Sharing (CORS).
* **Container Registry:** Amazon Elastic Container Registry (ECR) for backend and frontend Docker images.
* **Cluster Orchestration:** Amazon Elastic Kubernetes Service (AWS EKS v1.31) provisioned with Terraform, leveraging Kustomize for declarative GitOps updates.
* **CI/CD Automation:** GitHub Actions workflows executing dependency caching, linting, testing, image packaging, and zero-downtime rolling releases.

---

## 🚀 CI/CD Pipeline Implementation

### 1. Frontend Continuous Integration (`frontend-ci.yaml`)
Triggered on pull requests targeting `main` and via `workflow_dispatch`:
* **Lint Job:**
  * Node.js 18 setup.
  * **Cache Validation:** Validates and caches `~/.npm` dependencies using `actions/cache@v3` prior to installation.
  * Dependency installation via `npm ci` followed by ESLint verification (`npm run lint`).
* **Test Job:**
  * Node.js 18 setup.
  * **Cache Validation:** Validates `~/.npm` dependency cache with `actions/cache@v3`.
  * Executes Jest test suites in non-interactive mode (`npm test -- --watchAll=false`).
* **Build Job (requires `[lint, test]`):**
  * Node.js 18 setup.
  * **Cache Validation:** Validates `~/.npm` dependency cache with `actions/cache@v3`.
  * Production bundle compilation verified via `npm run build`.

### 2. Backend Continuous Deployment (`backend-cd.yaml`)
Triggered on push to `main` modifying `starter/backend/**` and via `workflow_dispatch`:
* Executes Python code standards validation (`flake8`) and test suites (`pytest`) under Pipenv.
* Authenticates with AWS ECR via `aws-actions/amazon-ecr-login@v1`.
* Builds, tags, and pushes backend Docker images to Amazon ECR.
* Updates the Kubernetes deployment image with `kustomize edit set image` and applies the manifest.
* **Deployment Verification & Logging:**
  * Performs rollout status verification: `kubectl rollout status deployment/backend --timeout=180s`.
  * Emits full cluster state: `kubectl get all`.
  * Emits deployment metadata: `kubectl describe deploy backend`.
  * Validates ECR image details: `aws ecr describe-images --repository-name backend --image-ids imageTag=latest`.

### 3. Frontend Continuous Deployment (`frontend-cd.yaml`)
Triggered on push to `main` modifying `starter/frontend/**` and via `workflow_dispatch`:
* Executes cached dependency installations (`actions/cache@v3`), ESLint checks, and Jest tests.
* Builds the production Docker image with build-arg injection:
  `--build-arg REACT_APP_MOVIE_API_URL=${{ secrets.REACT_APP_MOVIE_API_URL }}`
* Pushes the compiled frontend container image to Amazon ECR.
* Deploys the service to AWS EKS using Kustomize.
* **Deployment Verification & Logging:**
  * Verifies rollout health: `kubectl rollout status deployment/frontend --timeout=180s`.
  * Emits full cluster state: `kubectl get all`.
  * Emits deployment metadata: `kubectl describe deploy frontend`.
  * Validates ECR image details: `aws ecr describe-images --repository-name frontend --image-ids imageTag=latest`.

---

## 🔐 GitHub Repository Secrets Configuration

The following repository secrets are configured under **Settings > Secrets and variables > Actions**:

| Secret Name | Value / Description |
| :--- | :--- |
| `AWS_ACCESS_KEY_ID` | AWS IAM Access Key ID |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM Secret Access Key |
| `AWS_SESSION_TOKEN` | AWS STS Session Token (for Learner Lab sessions) |
| `AWS_DEFAULT_REGION` | `us-east-1` |
| `EKS_CLUSTER_NAME` | `cluster` |
| `BACKEND_ECR_REPO` | `backend` |
| `FRONTEND_ECR_REPO` | `frontend` |
| `REACT_APP_MOVIE_API_URL` | `http://ac5162dc1ec0246df954778921947962-2026922502.us-east-1.elb.amazonaws.com` |

---

## 💻 Local Development & Testing

### Frontend
```bash
cd starter/frontend

# Install dependencies
npm ci

# Run linter & test suite
npm run lint
npm test -- --watchAll=false

# Build production bundle
npm run build

# Start local server
REACT_APP_MOVIE_API_URL=http://localhost:5000 npm start