# Birthday Service
A small **FastAPI** microservice that stores a user's name and date of birth and greets them when they visit.

```
PUT  /hello/<username>   # save / update birthday
GET  /hello/<username>   # greet the user
```

---
## Features
* **FastAPI + SQLAlchemy 2.0 (async)**  
* **Alembic** migrations (async‑ready)  
* Production‑ready **Docker** image (uvicorn‑gunicorn)  
* **Helm 3** chart with rolling updates, probes, HPA, Ingress/NLB/ALB  
* Runs locally with **Docker Compose** or **Minikube**  
* Deployed to **AWS EKS** (ALB Ingress Controller)

---
## API
| Method & Path                      | Description                                   | Success Codes |
|------------------------------------|-----------------------------------------------|---------------|
| `PUT  /hello/{username}`           | Save or update date of birth *(YYYY‑MM‑DD)*   | `204`         |
| `GET  /hello/{username}`           | Greet user, show days until birthday          | `200`, `404`  |

`<username>` — only latin letters.  
`dateOfBirth`  must be **\< today**.

---
## Local Run (no AWS)
### 1. Clone & prepare
```bash
git clone https://github.com/sshishkin/bday-service.git
cd bday-service
```

### 2. Quick run with Docker Compose (PostgreSQL)
```bash
docker compose up           # http://localhost:8000
```
The stack brings up `postgres` + the service.  
Open <http://localhost:8000/docs> for Swagger UI.

### 3. Dev loop with Poetry + SQLite (no DB server)
```bash
poetry install --with dev
export DATABASE_URL="sqlite+aiosqlite:///./dev.db"
poetry run alembic upgrade head
poetry run uvicorn bday_service.app:app --reload
```

### 4. Run tests
```bash
poetry run pytest -v --color=yes
```
Tests automatically switch to `sqlite:///./test.db`, create tables on‑the‑fly and clean up after.


---
## Kubernetes (Minikube)
```bash
minikube start
minikube addons enable ingress
helm upgrade --install bday ./helm \
    --set image.repository="docker.io/tcp22/bday" \
    --set secret.value="postgresql+asyncpg://login:password@hostname:5432/postgres" \
    --set ingress.hostname="bday.test.local" 

# add to /etc/hosts
$(minikube ip) bday.test.local
open http://bday.test.local/hello/Health
```

---
## AWS EKS Deployment
### Prerequisites
* `eksctl`, `kubectl`, `helm`, `aws` CLI logged in
* An EKS cluster (❯ `eksctl create cluster ...`)
* OIDC provider + IAM role for **AWS Load Balancer Controller**

### 1. Install AWS Load Balancer Controller
```bash
helm repo add eks https://aws.github.io/eks-charts
eksctl utils associate-iam-oidc-provider --cluster <cluster> -y
eksctl create iamserviceaccount \
  --cluster <cluster> --namespace kube-system \
  --name aws-load-balancer-controller \
  --attach-policy-arn arn:aws:iam::<ACCOUNT>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=<cluster> \
  --set serviceAccount.name=aws-load-balancer-controller
```

### 2. Create secret with DB URL
```bash
kubectl create secret generic db-secret \
  --from-literal=DATABASE_URL="postgresql+asyncpg://user:pass@<rds-endpoint>:5432/proddb"
```

### 3. Deploy chart
```bash
helm upgrade --install bday ./helm \
  --set image.repository=docker.io/tcp22/bday \
  --set image.tag=<IMAGE_TAG> \
  --set secret.value="postgresql+asyncpg://login:password@hostname:5432/postgres" \
  --set ingress.hostname=bday.example.com \
  --set ingress.controller=alb
```
Controller creates **ALB**. Its hostname can be viewed with:
```bash
kubectl get ingress bday -n default -w
```
### 4. DNS
* Create **CNAME / Route53 ALIAS** `bday.example.com → <alb‑dns>.amazonaws.com`.
* After a few minutes, you can access the service at `http://bday.example.com/hello/Health`.
