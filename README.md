# Serverless Portfolio Architecture (AWS)

**Live Link:** [View my Live Resume](https://dzcey4h6erix0.cloudfront.net)

## Project Overview
This repository houses the architecture and source code for a production-ready, serverless cloud resume. The objective was to move beyond basic static hosting by building a secure, event-driven system that handles dynamic visitor telemetry and automated contact routing. By leveraging a fully serverless stack, the site achieves high availability and global performance while maintaining a near-zero cost footprint.

## System Architecture
<img width="1540" height="1230" alt="System Architectue" src="https://github.com/user-attachments/assets/302a35dc-f106-4d65-963a-fdf12e1a32d3" />

## Architecture & Technical Implementation

### Frontend & Global Delivery
* **Storage (Amazon S3):** Static assets are hosted in a private bucket with all public access blocked.
* **CDN (Amazon CloudFront):** Acts as the global entry point, serving content via HTTPS to minimize latency.
* **Origin Security:** Implemented **Origin Access Control (OAC)**. The S3 bucket policy is restricted to CloudFront service principals only, ensuring the origin is invisible to the public internet.

### Serverless Backend (Python & Boto3)
* **API Layer:** Amazon API Gateway (HTTP API). Configured with custom **CORS** policies to securely bridge the frontend domain with backend resources.
* **Compute (AWS Lambda):**
    * `visitor-counter-function.py`: Manages site telemetry.
    * `contact-form-function.py`: Parses JSON payloads and routes messages to SES.
* **Persistence (Amazon DynamoDB):** A NoSQL table using **Atomic Increments** to ensure accurate visitor tracking during concurrent requests.
* **Communications:** Amazon SES (Simple Email Service) configured with a verified identity to handle automated outbound routing.

### Security & Operational Excellence
* **IAM Governance:** Applied the **Principle of Least Privilege**. Lambda execution roles are strictly scoped to the ARNs of the DynamoDB table and SES identity.
* **Cost Optimization:** Established **AWS Budget** alerts at a **$0.01 threshold** to demonstrate fiscal responsibility and prevent "surprise" costs.
* **Edge Caching:** Managed the content lifecycle using manual CloudFront invalidations (`/*`) to ensure global updates are reflected immediately.

### Technical Challenges & Troubleshooting
* **CORS Resolution:** Handled `Access-Control-Allow-Origin` and pre-flight `OPTIONS` requests within API Gateway to resolve browser-side blocking.
* **Payload Decoding:** Resolved integration issues by implementing robust event body parsing in Lambda to decode stringified JSON objects sent via the JavaScript `fetch()` API.
