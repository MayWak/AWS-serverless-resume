# Serverless Portfolio Architecture (AWS)

**Live Link:** [View my Live Resume](https://dzcey4h6erix0.cloudfront.net)

## Project Overview
This repository contains the infrastructure and code for a serverless portfolio website. The project transitions a traditional static site into a global, event-driven application with real-time visitor tracking and an integrated contact system.

## System Architecture

```mermaid
graph TD
    %% Node Definitions
    User((🌐 User / Browser))
    
    subgraph Edge ["Phase I: Global Edge & Perimeter"]
        CF["<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/NetworkingContentDelivery/CloudFront.png' width='40'/><br/>Amazon CloudFront"]
        OAC{{"Origin Access Control (OAC)"}}
        S3[("<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/Storage/SimpleStorageService.png' width='40'/><br/>Private S3 Bucket")]
    end

    subgraph Backend ["Phase II: Serverless Compute"]
        API["<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/ApplicationIntegration/APIGateway.png' width='40'/><br/>API Gateway (HTTP API)"]
        Lambda["<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/Compute/Lambda.png' width='40'/><br/>AWS Lambda (Python)"]
    end

    subgraph Persistence ["Phase III: Data & Communication"]
        DDB[("<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/Database/DynamoDB.png' width='40'/><br/>Amazon DynamoDB")]
        SES["<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/BusinessApplications/SimpleEmailService.png' width='40'/><br/>Amazon SES"]
    end

    subgraph Management ["Operational Excellence"]
        CW["<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/ManagementGovernance/CloudWatch.png' width='40'/><br/>CloudWatch Logs"]
        Budget["<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/ManagementGovernance/Budgets.png' width='40'/><br/>AWS Budgets ($0.01)"]
        IAM["<img src='https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist/SecurityIdentityCompliance/IAM.png' width='40'/><br/>IAM Roles (Least Privilege)"]
    end

    %% Connection Logic
    User -->|1. HTTPS Request| CF
    CF -->|2. Secure Fetch| OAC
    OAC -.->|3. Origin Access| S3
    S3 -.->|4. Static Assets| CF
    CF -->|5. Render HTML/CSS/JS| User

    User -->|6. JS Fetch API| API
    API -->|7. Trigger| Lambda
    Lambda -->|8. Update Counter| DDB
    Lambda -->|9. Send Contact Email| SES

    %% Operational Links
    Lambda -.->|Logs| CW
    API -.->|Logs| CW
    IAM -.->|Permissions| Lambda
    Budget -.->|Guardrails| Backend
    
    %% Styling
    style Edge fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Backend fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Persistence fill:#efebe9,stroke:#4e342e,stroke-width:2px
    style Management fill:#fff3e0,stroke:#e65100,stroke-dasharray: 5 5
    style OAC fill:#fff,stroke:#d32f2f,stroke-width:2px
```

### Frontend & Global Delivery
* **Host:** Amazon S3 (Private Bucket).
* **CDN:** Amazon CloudFront.
* **Origin Security:** Implemented Origin Access Control (OAC). The S3 bucket policy is restricted to CloudFront service principals only, preventing direct S3 URL access and ensuring all traffic is encrypted via HTTPS.

### Backend Services (Python/Boto3)
* **API Layer:** Amazon API Gateway (HTTP API). Handles CORS headers to permit cross-domain requests from the CloudFront distribution.
* **Database:** Amazon DynamoDB. Stores visitor telemetry using an atomic counter to ensure data integrity during concurrent hits.
* **Compute:** * `visitor-counter-function.py`: Increments and retrieves site view counts.
    * `contact-form-functio.py`: Parses JSON payloads and triggers email delivery via Amazon SES.
* **Communication:** Amazon SES (Simple Email Service) configured with verified identity for secure form routing.

## Security & Operations
* **IAM Policy:** Followed the principle of least privilege for Lambda execution roles, scoping permissions to specific Resource ARNs (DynamoDB table and SES identity).
* **Cost Management:** Established AWS Budget alerts at a $0.01 threshold to monitor resource consumption in real-time.
* **Caching:** Configured manual CloudFront invalidations (/*) to manage content updates across edge locations.

## Technical Notes & Troubleshooting
* **CORS Management:** Managed Access-Control-Allow-Origin and Access-Control-Allow-Methods (OPTIONS, POST) within API Gateway to resolve browser-side blocking issues during the integration phase.
* **Event Parsing:** Configured Lambda handlers to properly decode event['body'] strings sent from the frontend fetch() API.
