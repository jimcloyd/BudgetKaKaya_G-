# AWS Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Internet Users                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Route 53 (Optional)                           │
│                    yourdomain.com                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        │ Frontend                                │ Backend
        ▼                                         ▼
┌──────────────────┐                    ┌──────────────────┐
│   CloudFront     │                    │  Elastic         │
│   (CDN + HTTPS)  │                    │  Beanstalk       │
│   (Optional)     │                    │  Load Balancer   │
└────────┬─────────┘                    └────────┬─────────┘
         │                                       │
         │                                       │
         ▼                                       ▼
┌──────────────────┐                    ┌──────────────────┐
│   Amazon S3      │                    │  EC2 Instances   │
│   Static Website │                    │  (Auto Scaling)  │
│   Hosting        │                    │                  │
│                  │                    │  Flask App       │
│  - index.html    │                    │  + Gunicorn      │
│  - React App     │                    │                  │
│  - CSS/JS        │                    └────────┬─────────┘
└──────────────────┘                             │
                                                 │
                                                 │ PostgreSQL
                                                 │ Protocol
                                                 ▼
                                        ┌──────────────────┐
                                        │   Amazon RDS     │
                                        │   PostgreSQL     │
                                        │                  │
                                        │  - Users         │
                                        │  - Expenses      │
                                        │  - Budgets       │
                                        │  - Categories    │
                                        └──────────────────┘
                                                 │
                                                 │ Encrypted
                                                 ▼
                                        ┌──────────────────┐
                                        │  RDS Automated   │
                                        │  Backups         │
                                        └──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AWS Secrets Manager                           │
│  - Database Credentials                                          │
│  - JWT Secret Keys                                               │
│  - Flask Secret Keys                                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    CloudWatch (Monitoring)                       │
│  - Application Logs                                              │
│  - Performance Metrics                                           │
│  - Alarms & Notifications                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Network Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Region (us-east-1)                   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    VPC (10.0.0.0/16)                       │ │
│  │                                                            │ │
│  │  ┌──────────────────────┐  ┌──────────────────────┐      │ │
│  │  │  Public Subnet 1     │  │  Public Subnet 2     │      │ │
│  │  │  (10.0.1.0/24)       │  │  (10.0.2.0/24)       │      │ │
│  │  │  AZ: us-east-1a      │  │  AZ: us-east-1b      │      │ │
│  │  │                      │  │                      │      │ │
│  │  │  ┌────────────────┐  │  │  ┌────────────────┐  │      │ │
│  │  │  │ EC2 Instance   │  │  │  │ EC2 Instance   │  │      │ │
│  │  │  │ (EB App)       │  │  │  │ (EB App)       │  │      │ │
│  │  │  └────────────────┘  │  │  └────────────────┘  │      │ │
│  │  └──────────────────────┘  └──────────────────────┘      │ │
│  │            │                          │                   │ │
│  │            └──────────┬───────────────┘                   │ │
│  │                       │                                   │ │
│  │                       │ PostgreSQL (5432)                 │ │
│  │                       ▼                                   │ │
│  │  ┌──────────────────────┐  ┌──────────────────────┐      │ │
│  │  │  Private Subnet 1    │  │  Private Subnet 2    │      │ │
│  │  │  (10.0.11.0/24)      │  │  (10.0.12.0/24)      │      │ │
│  │  │  AZ: us-east-1a      │  │  AZ: us-east-1b      │      │ │
│  │  │                      │  │                      │      │ │
│  │  │  ┌────────────────┐  │  │  ┌────────────────┐  │      │ │
│  │  │  │ RDS Primary    │  │  │  │ RDS Standby    │  │      │ │
│  │  │  │ (Multi-AZ)     │◄─┼──┼─►│ (Failover)     │  │      │ │
│  │  │  └────────────────┘  │  │  └────────────────┘  │      │ │
│  │  └──────────────────────┘  └──────────────────────┘      │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Security Groups

```
┌─────────────────────────────────────────────────────────────────┐
│  Internet Gateway                                                │
│  (0.0.0.0/0)                                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS (80/443)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Load Balancer Security Group                                    │
│  Inbound:                                                        │
│  - Port 80 from 0.0.0.0/0                                        │
│  - Port 443 from 0.0.0.0/0 (if HTTPS)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP (80)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  EC2 Instance Security Group (Elastic Beanstalk)                 │
│  Inbound:                                                        │
│  - Port 80 from Load Balancer SG                                 │
│  Outbound:                                                       │
│  - Port 5432 to RDS SG                                           │
│  - Port 443 to Internet (for AWS API calls)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ PostgreSQL (5432)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  RDS Security Group                                              │
│  Inbound:                                                        │
│  - Port 5432 from EC2 Instance SG only                           │
│  Outbound:                                                       │
│  - None (database doesn't initiate connections)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### User Registration/Login Flow

```
User Browser
    │
    │ 1. POST /api/auth/register
    ▼
CloudFront (Optional)
    │
    │ 2. Forward to origin
    ▼
S3 Static Website
    │
    │ 3. Load React App
    ▼
React App
    │
    │ 4. API Call: POST /api/auth/register
    ▼
Elastic Beanstalk Load Balancer
    │
    │ 5. Route to healthy instance
    ▼
EC2 Instance (Flask App)
    │
    │ 6. Hash password, create user
    ▼
RDS PostgreSQL
    │
    │ 7. Store user record
    ▼
EC2 Instance (Flask App)
    │
    │ 8. Generate JWT token
    ▼
React App
    │
    │ 9. Store token, redirect to dashboard
    ▼
User Browser
```

### Expense Creation Flow

```
User Browser (Authenticated)
    │
    │ 1. POST /api/expenses (with JWT)
    ▼
React App
    │
    │ 2. Add Authorization header
    ▼
Elastic Beanstalk
    │
    │ 3. Verify JWT token
    ▼
EC2 Instance (Flask App)
    │
    │ 4. Validate expense data
    │ 5. Check shared account access
    ▼
RDS PostgreSQL
    │
    │ 6. Insert expense record
    │ 7. Update category totals
    ▼
EC2 Instance (Flask App)
    │
    │ 8. Return expense with ID
    ▼
React App
    │
    │ 9. Update UI, show success
    ▼
User Browser
```

## Scaling Strategy

### Horizontal Scaling (Auto Scaling)

```
Low Traffic:
┌──────────────┐
│ EC2 Instance │  (1 instance)
└──────────────┘

Medium Traffic:
┌──────────────┐  ┌──────────────┐
│ EC2 Instance │  │ EC2 Instance │  (2 instances)
└──────────────┘  └──────────────┘

High Traffic:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ EC2 Instance │  │ EC2 Instance │  │ EC2 Instance │  │ EC2 Instance │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
                        (4 instances)
```

### Vertical Scaling (Instance Types)

```
Development:   t3.micro   (2 vCPU, 1 GB RAM)   ~$7/month
Production:    t3.small   (2 vCPU, 2 GB RAM)   ~$15/month
High Load:     t3.medium  (2 vCPU, 4 GB RAM)   ~$30/month
```

## Disaster Recovery

### Backup Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  RDS Automated Backups                                           │
│  - Daily snapshots (7 day retention)                             │
│  - Point-in-time recovery                                        │
│  - Stored in S3 (encrypted)                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Manual Snapshots                                                │
│  - Before major updates                                          │
│  - Long-term retention                                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Application Code                                                │
│  - Git repository (GitHub/GitLab)                                │
│  - EB application versions                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Frontend Assets                                                 │
│  - S3 versioning enabled                                         │
│  - CloudFront cache                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Recovery Time Objectives (RTO)

- **Database Failure**: ~5-10 minutes (RDS Multi-AZ automatic failover)
- **Application Failure**: ~2-5 minutes (Auto Scaling + Health Checks)
- **Region Failure**: ~1-2 hours (Manual failover to backup region)
- **Data Corruption**: ~30-60 minutes (Restore from snapshot)

## Cost Breakdown

```
Monthly Costs (Estimated):

┌─────────────────────────────────────────────────────────────────┐
│  Service              │  Configuration      │  Monthly Cost     │
├───────────────────────┼─────────────────────┼───────────────────┤
│  RDS PostgreSQL       │  db.t3.micro        │  $15-20           │
│  Elastic Beanstalk    │  t3.small (1-2)     │  $15-30           │
│  S3 Storage           │  5 GB               │  $1-2             │
│  S3 Data Transfer     │  10 GB/month        │  $1-2             │
│  CloudFront (opt)     │  10 GB/month        │  $1-5             │
│  Route 53 (opt)       │  1 hosted zone      │  $0.50            │
│  Secrets Manager      │  2 secrets          │  $1               │
│  CloudWatch           │  Basic monitoring   │  $0-5             │
├───────────────────────┴─────────────────────┼───────────────────┤
│  TOTAL (Basic)                              │  $35-45/month     │
│  TOTAL (with CloudFront + Domain)           │  $40-60/month     │
└─────────────────────────────────────────────┴───────────────────┘

Free Tier Eligible (First 12 months):
- RDS: 750 hours/month of db.t2.micro
- EC2: 750 hours/month of t2.micro
- S3: 5 GB storage, 20,000 GET requests
- CloudFront: 50 GB data transfer out
```

## Monitoring & Alerts

```
CloudWatch Metrics:

┌─────────────────────────────────────────────────────────────────┐
│  RDS Metrics                                                     │
│  - CPU Utilization (Alert > 80%)                                 │
│  - Free Storage Space (Alert < 2 GB)                             │
│  - Database Connections (Alert > 80% of max)                     │
│  - Read/Write Latency                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Elastic Beanstalk Metrics                                       │
│  - Instance Health (Alert if unhealthy)                          │
│  - Application Requests (5xx errors)                             │
│  - Response Time (Alert > 2 seconds)                             │
│  - CPU Utilization (Alert > 80%)                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Application Logs                                                │
│  - Flask application logs                                        │
│  - Gunicorn access logs                                          │
│  - Database query logs                                           │
│  - Error tracking (Sentry integration optional)                  │
└─────────────────────────────────────────────────────────────────┘
```
