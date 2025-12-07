\# Online Exam System - Microservices Architecture



This project is a scalable, event-driven Online Exam System built with Microservices architecture, deployed on Kubernetes, and monitored via Prometheus \& Grafana.



\## 🚀 Architecture Overview

The system consists of 4 main microservices communicating synchronously (REST API) and asynchronously (RabbitMQ):



1\.  \*\*Identity Service:\*\* User authentication \& JWT management (FastAPI + PostgreSQL).

2\.  \*\*Exam Service:\*\* Creating and listing exams (FastAPI + PostgreSQL).

3\.  \*\*Submit Service:\*\* Handling exam submissions and queuing them (FastAPI + RabbitMQ).

4\.  \*\*Grading Service:\*\* Background worker that consumes submissions and calculates scores (Python Worker).



\## 🛠️ Tech Stack

\* \*\*Backend:\*\* Python, FastAPI

\* \*\*Database:\*\* PostgreSQL

\* \*\*Message Broker:\*\* RabbitMQ

\* \*\*Containerization:\*\* Docker

\* \*\*Orchestration:\*\* Kubernetes (K8s)

\* \*\*CI/CD:\*\* GitHub Actions (Automated Build \& Push to Docker Hub)

\* \*\*Monitoring:\*\* Prometheus \& Grafana



\## 📂 Project Structure

\* `/k8s`: Kubernetes Deployment and Service YAML files.

\* `/.github/workflows`: CI/CD Pipeline configuration.

\* `/identity-service`: Auth microservice code.

\* `/exam-service`: Exam management microservice code.

\* `/submit-service`: Submission handler microservice code.

\* `/grading-service`: Worker service code.



\## ⚙️ How to Run

1\.  \*\*Clone the repo:\*\*

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/sevimbahadiir/online-exam-system.git](https://github.com/sevimbahadiir/online-exam-system.git)

&nbsp;   cd online-exam-system

&nbsp;   ```



2\.  \*\*Deploy to Kubernetes:\*\*

&nbsp;   ```bash

&nbsp;   kubectl apply -f k8s/

&nbsp;   ```



3\.  \*\*Access Services:\*\*

&nbsp;   \* Identity Service: `http://localhost:8000`

&nbsp;   \* Exam Service: `http://localhost:8001`

&nbsp;   \* Submit Service: `http://localhost:8002`

&nbsp;   \* Grafana Dashboard: `http://localhost:3000`

