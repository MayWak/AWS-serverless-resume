# AWS Serverless Cloud Resume ☁️
**Live Demo:** [PASTE_YOUR_CLOUDFRONT_URL_HERE]

## 🎯 Project Overview
This project is a full-stack, serverless web application designed to host a professional resume while demonstrating core architectural principles on AWS. The goal was to build a secure, highly available, and cost-efficient system that handles global content delivery and serverless backend logic.

## 🏗️ Architecture Diagram
*(I recommend adding a diagram later using tools like Draw.io or Lucidchart)*

The request flow:
**User** → **CloudFront (HTTPS)** → **S3 (Private Origin)**
**User** → **API Gateway** → **Lambda** → **DynamoDB / SES**

---

## 🛠️ Technical Breakdown (The SAA Perspective)

### 1. Edge Networking & Security (The Perimeter)
* **Amazon CloudFront:** Used as a Global Content Delivery Network (CDN) to ensure low-latency access via edge locations.
* **Origin Access Control (OAC):** Implemented to secure the S3 origin. The S3 bucket is completely private; access is granted strictly to the CloudFront service principal via a tailored **IAM Resource Policy**.
* **SSL/TLS:** Enforced HTTPS delivery using default CloudFront certificates to ensure data-in-transit security.

### 2. Serverless Backend (Event-Driven Design)
* **Amazon API Gateway (HTTP API):** Acts as the entry point for the backend. Configured with **CORS (Cross-Origin Resource Sharing)** policies to allow secure communication between the CloudFront domain and the API.
* **AWS Lambda (Python/Boto3):**
    * **Telemetry Function:** Interacts with DynamoDB using atomic increments to track real-time visitor counts without race conditions.
    * **Communication Function:** Parses user input and routes messages through **Amazon SES**.
* **Amazon DynamoDB:** A fully managed NoSQL database chosen for its seamless scalability and high performance.

### 3. Operational Excellence & Cost Governance
* **AWS Budgets:** To demonstrate fiscal responsibility, I implemented a budget alert at the **$0.01 threshold**, ensuring real-time notification of any unexpected cost spikes.
* **CloudWatch Logs:** Utilized for debugging and monitoring Lambda execution health and API request flows.

---

## 🧠 Challenges Overcome
* **CORS Troubleshooting:** Resolved "Access-Control-Allow-Origin" headers between the frontend and API Gateway to enable smooth cross-domain fetching.
* **Identity & Access Management:** Crafted least-privilege IAM policies to ensure Lambda functions only have permissions for the specific DynamoDB table and SES identities required.

## 🚀 Skills Demonstrated
`Solutions Architecture` `IAM Security` `Serverless Computing (FaaS)` `NoSQL Database Design` `CDN & Edge Networking` `Cost Management`
