# Serverless Portfolio Architecture (AWS)

**Live Link:** [View my Live Resume](https://dzcey4h6erix0.cloudfront.net)

## Project Overview
This repository contains the infrastructure and code for a serverless portfolio website. The project transitions a traditional static site into a global, event-driven application with real-time visitor tracking and an integrated contact system.

## System Architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ff9900', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff'}}}%%
graph LR
    %% --- MAIN TITLE ---
    %% This acts as a header within the diagram itself
    Title[<b style='font-size:20px'>AWS Serverless Cloud Resume Architecture</b><br/>Production-Grade, Secure, Cost-Optimized]:::title --> Subtitle:::subtitle
    Subtitle[Adhering to AWS Well-Architected Framework]:::subtitle

    %% --- NODES & USERS ---
    User(<i class="fa fa-user fa-2x"></i><br/>End User / Recruiter):::user

    %% --- PHASE I: FRONTEND & EDGE ---
    subgraph EdgePerimeter [Phase I: Global Edge Perimeter]
        direction TB
        CF(🌐 Amazon CloudFront<br/>Global CDN / 600+ PoPs):::network
        OAC{<i class="fa fa-shield-alt"></i><br/>Origin Access Control<br/>SigV4 Security}:::security
        S3Bucket(<i class="fa fa-database"></i><br/>Private S3 Bucket<br/>Static Assets: index.html):::storage
    end

    %% --- PHASE II: BACKEND ---
    subgraph ComputeLayer [Phase II: Serverless Backend]
        direction TB
        APIGW(<i class="fa fa-api"></i><br/>Amazon API Gateway<br/>HTTP API endpoint):::compute
        CORS{<i class="fa fa-handshake"></i><br/>CORS<br/>Configuration}:::security
        
        subgraph LambdaLogic [Python 3.x / Boto3 SDK]
            direction LR
            Func1(<i class="fa fa-code"></i><br/>Lambda: Visitor Counter<br/>Atomic Increment):::compute
            Func2(<i class="fa fa-envelope"></i><br/>Lambda: Contact Handler<br/>JSON Parser):::compute
        end
    end

    %% --- PHASE III: DATA ---
    subgraph DataMessaging [Phase III: Persistence & Messaging]
        direction TB
        DDB(<i class="fa fa-table"></i><br/>Amazon DynamoDB<br/>NoSQL / Single-Table):::storage
        SES(<i class="fa fa-paper-plane"></i><br/>Amazon SES<br/>Simple Email Service):::messaging
    end

    %% --- OPERATIONAL EXCELLENCE & SECURITY ---
    subgraph Governance [Operational Excellence & Security]
        direction BT
        IAM(<i class="fa fa-key"></i><br/>AWS IAM<br/>Least Privilege Roles):::security
        CW(<i class="fa fa-eye"></i><br/>Amazon CloudWatch<br/>Logs & Metrics):::observability
        Budget(<i class="fa fa-chart-line"></i><br/>AWS Budgets<br/>Threshold: $0.01):::governance
    end

    %% --- DEFINING THE FLOW & INTERACTION ---
    
    %% 1. Static Asset Request
    User -- "1. Requests Website<br/>(HTTPS/TLS)" --> CF
    CF -- "2. Authenticates Request<br/>(SigV4 via OAC)" --> OAC
    OAC -- "3. Fetches Assets<br/>(Private Origin)" --> S3Bucket
    S3Bucket -- "4. Returns index.html" --> CF
    CF -- "5. Delivers Content<br/>(Low-Latency)" --> User

    %% 2. Dynamic API Request
    User -- "6. Executes JS fetch()" --> APIGW
    APIGW -.-> CORS
    CORS -- "7. Validates Origin" --> APIGW
    
    %% Triggering Logic
    APIGW -- "8. Triggers<br/>(Event Payload)" --> LambdaLogic
    
    %% Lambda Interactions
    Func1 -- "9. UpdateItem<br/>(Atomic Increment)" --> DDB
    Func2 -- "10. SendEmail<br/>(Verified Identity)" --> SES

    %% 3. Cross-Cutting Support
    IAM -. "Enforces<br/>Permissions" .-> LambdaLogic
    IAM -. "Enforces<br/>Permissions" .-> S3Bucket
    LambdaLogic -- "Streams Logs" --> CW
    APIGW -- "Streams Logs" --> CW
    Governance -. "Monitors<br/>Spend" .-> User

    %% --- COMPONENT STYLING ---
    classDef title fill:none,stroke:none,color:#232F3E,font-weight:bold;
    classDef subtitle fill:none,stroke:none,color:#666,font-style:italic;
    classDef user fill:#fff,stroke:#232F3E,stroke-width:2px,color:#232F3E,rx:10,ry:10;
    
    %% AWS Service Colors
    classDef network fill:#8C4FFF,stroke:#fff,stroke-width:1px,color:#fff,rx:5,ry:5;
    classDef compute fill:#FF9900,stroke:#fff,stroke-width:1px,color:#fff,rx:5,ry:5;
    classDef storage fill:#3B48CC,stroke:#fff,stroke-width:1px,color:#fff,rx:5,ry:5;
    classDef messaging fill:#41B13F,stroke:#fff,stroke-width:1px,color:#fff,rx:5,ry:5;
    
    classDef security fill:#E05243,stroke:#fff,stroke-width:1px,color:#fff,rx:15,ry:15;
    classDef observability fill:#20BCD5,stroke:#fff,stroke-width:1px,color:#fff,rx:5,ry:5;
    classDef governance fill:#545B64,stroke:#fff,stroke-width:1px,color:#fff,rx:5,ry:5;

    %% Link Styling (Enthusiastic & Sharp)
    linkStyle default stroke:#545B64,stroke-width:1px,stroke-dasharray: 3 3;
    linkStyle 0,1,2,3,4 stroke:#8C4FFF,stroke-width:2px,stroke-dasharray: 0;
    linkStyle 5,6,7,8 stroke:#FF9900,stroke-width:2px,stroke-dasharray: 0;
    linkStyle 9,10 stroke:#3B48CC,stroke-width:2px,stroke-dasharray: 0;
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
