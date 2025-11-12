# AWS Deployment Checklist

Use this checklist to ensure you complete all deployment steps correctly.

## Pre-Deployment

- [ ] AWS account created and verified
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] EB CLI installed (`pip install awsebcli`)
- [ ] Node.js and npm installed
- [ ] Python 3.9+ installed
- [ ] Git repository is up to date

## Infrastructure Setup

### Database (RDS)
- [ ] RDS PostgreSQL instance created
- [ ] Database endpoint noted
- [ ] Master username and password saved securely
- [ ] Database is in "Available" state
- [ ] Security group configured (will be done after EB setup)

### Secrets Management
- [ ] Database credentials stored in AWS Secrets Manager
- [ ] JWT secret key generated and stored
- [ ] Flask secret key generated and stored

### Backend (Elastic Beanstalk)
- [ ] EB application initialized (`eb init`)
- [ ] EB environment created (`eb create`)
- [ ] Environment variables configured:
  - [ ] `FLASK_ENV=production`
  - [ ] `DATABASE_URL` set correctly
  - [ ] `JWT_SECRET_KEY` set
  - [ ] `SECRET_KEY` set
- [ ] Application deployed (`eb deploy`)
- [ ] EB environment is "Green" status
- [ ] EB URL noted

### Security Groups
- [ ] RDS security group allows connections from EB security group
- [ ] EB security group allows HTTP (port 80) from internet
- [ ] Tested database connection from EB instance

### Database Migrations
- [ ] SSH'd into EB instance (`eb ssh`)
- [ ] Activated virtual environment
- [ ] Ran `flask db upgrade`
- [ ] Verified tables created in database

### Frontend (S3)
- [ ] S3 bucket created with unique name
- [ ] Static website hosting enabled
- [ ] Bucket policy set for public read access
- [ ] `.env.production` file created with correct API URL
- [ ] Frontend built (`npm run build`)
- [ ] Files uploaded to S3 (`aws s3 sync`)
- [ ] S3 website URL noted

### CORS Configuration
- [ ] Backend CORS updated to allow frontend domain
- [ ] Backend redeployed after CORS update

## Testing

### Backend API
- [ ] Health check endpoint responds: `curl http://YOUR_EB_URL/api/auth/login`
- [ ] Can register a new user
- [ ] Can login and receive JWT token
- [ ] Can create shared account
- [ ] Can create categories
- [ ] Can create expenses
- [ ] Can create budget limits
- [ ] Can view budget status

### Frontend
- [ ] Frontend loads without errors
- [ ] Can access registration page
- [ ] Can register new user
- [ ] Can login
- [ ] Can navigate between pages
- [ ] API calls work correctly
- [ ] No CORS errors in browser console

### Integration
- [ ] End-to-end user flow works:
  - [ ] Register → Login → Create shared account
  - [ ] Add expense → View in list
  - [ ] Set budget → See status
  - [ ] Logout → Login again

## Optional Enhancements

### CloudFront (CDN + HTTPS)
- [ ] CloudFront distribution created
- [ ] Origin set to S3 bucket
- [ ] Default root object set to `index.html`
- [ ] Custom error response configured (404 → /index.html)
- [ ] Distribution deployed (Status: Deployed)
- [ ] CloudFront URL tested
- [ ] Frontend redeployed with CloudFront URL

### SSL Certificate
- [ ] Certificate requested in ACM (us-east-1 region)
- [ ] DNS validation completed
- [ ] Certificate status: Issued
- [ ] Certificate attached to CloudFront distribution
- [ ] HTTPS working correctly

### Custom Domain
- [ ] Domain registered in Route 53 (or external registrar)
- [ ] Hosted zone created in Route 53
- [ ] A record (Alias) created pointing to CloudFront
- [ ] CNAME for www subdomain created
- [ ] DNS propagated (check with `nslookup`)
- [ ] Custom domain works with HTTPS

### Monitoring
- [ ] CloudWatch alarms set up for:
  - [ ] RDS CPU utilization
  - [ ] RDS storage space
  - [ ] EB instance health
  - [ ] Application errors
- [ ] SNS topic created for alerts
- [ ] Email subscription confirmed

### Backup
- [ ] RDS automated backups enabled (7 days retention)
- [ ] Manual RDS snapshot created
- [ ] S3 versioning enabled for frontend bucket
- [ ] Backend code backed up in Git

## Post-Deployment

### Documentation
- [ ] Deployment details documented
- [ ] Credentials stored securely (password manager)
- [ ] Team members notified of deployment
- [ ] User guide created (if needed)

### Security Review
- [ ] All secrets removed from code
- [ ] Environment variables verified
- [ ] Security groups reviewed (least privilege)
- [ ] RDS not publicly accessible
- [ ] HTTPS enforced (if using CloudFront)
- [ ] Strong passwords used everywhere

### Performance
- [ ] Page load times acceptable
- [ ] API response times acceptable
- [ ] Database queries optimized
- [ ] CloudFront caching working (if applicable)

### Cost Optimization
- [ ] Right-sized instance types
- [ ] RDS backup retention appropriate
- [ ] S3 lifecycle policies considered
- [ ] CloudWatch logs retention set
- [ ] Unused resources cleaned up

## Maintenance

### Regular Tasks
- [ ] Monitor CloudWatch metrics weekly
- [ ] Review RDS backups monthly
- [ ] Update dependencies quarterly
- [ ] Review AWS costs monthly
- [ ] Test disaster recovery plan quarterly

### Update Procedures
- [ ] Backend updates: `eb deploy`
- [ ] Frontend updates: `npm run build` + `aws s3 sync`
- [ ] Database migrations: `eb ssh` + `flask db upgrade`
- [ ] CloudFront cache invalidation after frontend updates

## Rollback Plan

### Backend Rollback
- [ ] Previous version identified: `eb appversion`
- [ ] Rollback command ready: `eb deploy --version VERSION_LABEL`

### Frontend Rollback
- [ ] S3 versioning enabled
- [ ] Previous version can be restored

### Database Rollback
- [ ] Recent snapshot available
- [ ] Restore procedure documented

## Emergency Contacts

- AWS Support: [Your support plan]
- Database Admin: [Contact]
- DevOps Lead: [Contact]
- On-Call Engineer: [Contact]

## Notes

Date Deployed: _______________
Deployed By: _______________
Version: _______________

Issues Encountered:
- 
- 
- 

Lessons Learned:
- 
- 
- 

---

**Status:** [ ] Not Started  [ ] In Progress  [ ] Completed  [ ] Issues

**Sign-off:** _______________  Date: _______________
