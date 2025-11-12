# Get Started with AWS Deployment

**Welcome!** This guide will help you deploy your Family Budget Tracker to AWS in the simplest way possible.

## What You'll Get

After following this guide, you'll have:
- ✅ A live web application accessible from anywhere
- ✅ Secure PostgreSQL database in the cloud
- ✅ Automatic backups
- ✅ HTTPS support (optional)
- ✅ Professional hosting infrastructure

**Estimated Time**: 30-45 minutes  
**Estimated Cost**: $35-60/month (or free for 12 months with AWS Free Tier)

## Before You Start

### 1. Create an AWS Account
- Go to [aws.amazon.com](https://aws.amazon.com)
- Click "Create an AWS Account"
- Follow the signup process
- **Important**: Enable MFA (Multi-Factor Authentication) for security

### 2. Install Required Tools

**AWS CLI** (Command Line Interface):
- Windows: Download from [AWS CLI Installer](https://awscli.amazonaws.com/AWSCLIV2.msi)
- Mac: `brew install awscli`
- Linux: `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install`

**EB CLI** (Elastic Beanstalk CLI):
```bash
pip install awsebcli
```

**Configure AWS CLI**:
```bash
aws configure
```
You'll need:
- AWS Access Key ID (get from AWS Console → IAM → Users → Security credentials)
- AWS Secret Access Key
- Default region: `us-east-1` (recommended)
- Default output format: `json`

### 3. Verify Installation

```bash
aws --version
eb --version
```

## Choose Your Deployment Method

### 🚀 Option 1: Automated Setup (Easiest)

**Best for**: First-time AWS users, quick deployment

```bash
# Make script executable (Linux/Mac only)
chmod +x aws-setup.sh

# Run the setup script
./aws-setup.sh
```

The script will:
1. Ask you a few questions
2. Create all AWS resources automatically
3. Deploy your application
4. Give you the URLs to access your app

**Time**: ~20 minutes (mostly waiting for AWS)

---

### 📋 Option 2: Step-by-Step Manual (Recommended for Learning)

**Best for**: Understanding what's happening, customization

Follow the **[AWS_QUICKSTART.md](AWS_QUICKSTART.md)** guide.

**Time**: ~30-45 minutes

---

### 🏗️ Option 3: Infrastructure as Code (Advanced)

**Best for**: Professional deployments, version control

Use CloudFormation template:

```bash
aws cloudformation create-stack \
    --stack-name family-budget-tracker \
    --template-body file://cloudformation-template.yaml \
    --parameters \
        ParameterKey=DBPassword,ParameterValue=YourStrongPassword123! \
        ParameterKey=S3BucketName,ParameterValue=your-unique-bucket-name-12345
```

**Time**: ~20 minutes

---

## After Deployment

### 1. Get Your Application URLs

**Backend API**:
```bash
cd backend
eb status
# Look for "CNAME" - that's your backend URL
```

**Frontend**:
```bash
aws s3 website s3://your-bucket-name
# Your frontend URL will be shown
```

### 2. Test Your Application

1. Open the frontend URL in your browser
2. Register a new account
3. Create a shared account
4. Add an expense
5. Set a budget limit

### 3. Set Up HTTPS (Recommended)

For production use, you should enable HTTPS:

1. Create a CloudFront distribution (see AWS_DEPLOYMENT_GUIDE.md)
2. Request an SSL certificate in AWS Certificate Manager
3. Update your frontend to use the CloudFront URL

## Common Issues & Solutions

### "Command not found: eb"
**Solution**: Install EB CLI: `pip install awsebcli`

### "Unable to connect to database"
**Solution**: Check RDS security group allows connections from EB instances
1. Go to AWS RDS Console
2. Click on your database
3. Click on the VPC security group
4. Edit inbound rules
5. Add PostgreSQL (5432) from EB security group

### "CORS error" in browser
**Solution**: Update backend CORS configuration
1. Edit `backend/app/__init__.py`
2. Add your frontend URL to CORS origins
3. Redeploy: `eb deploy`

### "502 Bad Gateway"
**Solution**: Check application logs
```bash
eb logs
```
Look for Python errors or database connection issues.

### Frontend shows blank page
**Solution**: Check browser console for errors
- Verify API URL in `.env.production`
- Check CORS configuration
- Verify backend is running: `eb status`

## Updating Your Application

### Update Backend Code
```bash
cd backend
# Make your changes
eb deploy
```

### Update Frontend Code
```bash
cd frontend
# Make your changes
npm run build
aws s3 sync dist/ s3://your-bucket-name --delete
```

Or use the deployment scripts:
```bash
./deploy-backend.sh
./deploy-frontend.sh your-bucket-name
```

## Monitoring Your Application

### Check Application Health
```bash
eb health
```

### View Logs
```bash
eb logs
```

### Monitor Costs
1. Go to AWS Console → Billing Dashboard
2. Set up billing alerts
3. Review Cost Explorer monthly

## Getting Help

### Documentation
- **Quick Start**: [AWS_QUICKSTART.md](AWS_QUICKSTART.md)
- **Detailed Guide**: [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)
- **Architecture**: [AWS_ARCHITECTURE.md](AWS_ARCHITECTURE.md)
- **Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

### AWS Support
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Forums](https://forums.aws.amazon.com/)
- [AWS Support Center](https://console.aws.amazon.com/support/)

### Troubleshooting
Check the troubleshooting section in [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)

## Cost Management

### Free Tier (First 12 Months)
- 750 hours/month of RDS db.t2.micro
- 750 hours/month of EC2 t2.micro
- 5 GB S3 storage
- 50 GB CloudFront data transfer

### After Free Tier
- **Minimal Setup**: ~$35/month
  - RDS db.t3.micro: $15
  - EB t3.small: $15
  - S3 + Transfer: $5

- **Production Setup**: ~$60/month
  - Includes CloudFront, custom domain, monitoring

### Reduce Costs
1. Use reserved instances (save 30-60%)
2. Stop development environments when not in use
3. Use smaller instance types for low traffic
4. Enable S3 lifecycle policies
5. Set up billing alerts

## Security Checklist

- [ ] Enable MFA on AWS account
- [ ] Use strong passwords (min 12 characters)
- [ ] Never commit secrets to Git
- [ ] Use AWS Secrets Manager for credentials
- [ ] Enable HTTPS (CloudFront + ACM)
- [ ] Keep dependencies updated
- [ ] Enable CloudTrail for audit logs
- [ ] Review security groups regularly
- [ ] Enable RDS encryption
- [ ] Set up automated backups

## Next Steps

After successful deployment:

1. **Set up monitoring**: Configure CloudWatch alarms
2. **Enable HTTPS**: Set up CloudFront with SSL
3. **Custom domain**: Register domain in Route 53
4. **CI/CD**: Set up GitHub Actions for automated deployments
5. **Backups**: Verify RDS automated backups are working
6. **Documentation**: Document your specific configuration
7. **Team access**: Set up IAM users for team members

## Quick Command Reference

```bash
# Backend
eb status              # Check environment status
eb logs                # View application logs
eb deploy              # Deploy new version
eb ssh                 # SSH into instance
eb health              # Check health status

# Frontend
npm run build          # Build for production
aws s3 sync dist/ s3://bucket --delete  # Deploy to S3

# Database
aws rds describe-db-instances  # Check RDS status
eb ssh                         # Then run migrations
flask db upgrade               # Run migrations

# Monitoring
aws cloudwatch get-metric-statistics  # Get metrics
eb health --refresh                   # Live health monitoring
```

## Success Checklist

- [ ] AWS account created and configured
- [ ] AWS CLI and EB CLI installed
- [ ] Backend deployed to Elastic Beanstalk
- [ ] Database created and migrations run
- [ ] Frontend deployed to S3
- [ ] Can register and login
- [ ] Can create expenses and budgets
- [ ] HTTPS enabled (optional but recommended)
- [ ] Monitoring set up
- [ ] Backups verified
- [ ] Team members have access
- [ ] Documentation updated

## Congratulations! 🎉

Your Family Budget Tracker is now live on AWS!

**Share your app**:
- Frontend: `http://your-bucket.s3-website-region.amazonaws.com`
- Or with CloudFront: `https://your-distribution.cloudfront.net`
- Or with custom domain: `https://yourdomain.com`

**Need help?** Check the other documentation files or open an issue.

---

**Remember**: AWS charges based on usage. Monitor your costs regularly and set up billing alerts!
