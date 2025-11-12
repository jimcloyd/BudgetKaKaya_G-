# GitHub Actions CI/CD Setup

## Overview

Your repository now has automatic deployment configured:
- **Push to Dev branch** → Automatically deploys to Dev environment
- **Push to Prod branch** → Automatically deploys to Production environment

## Setup Steps

### Step 1: Add AWS Credentials to GitHub Secrets

1. Go to your GitHub repository: https://github.com/jimcloyd/BudgetKaKaya_G-
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

#### AWS_ACCESS_KEY_ID
- Name: `AWS_ACCESS_KEY_ID`
- Value: Your AWS access key ID

#### AWS_SECRET_ACCESS_KEY
- Name: `AWS_SECRET_ACCESS_KEY`
- Value: Your AWS secret access key

#### DEV_BUCKET_SUFFIX (Optional - for dev environment)
- Name: `DEV_BUCKET_SUFFIX`
- Value: The random number from your dev bucket (e.g., `1234567890`)

### Step 2: Get Your AWS Credentials

If you don't have AWS credentials yet:

```powershell
# Check if you have credentials
aws configure list

# If not configured, create new access key:
# 1. Go to AWS Console: https://console.aws.amazon.com/iam/
# 2. Click your username (top right) → Security credentials
# 3. Scroll to "Access keys" → Create access key
# 4. Choose "Command Line Interface (CLI)"
# 5. Copy the Access Key ID and Secret Access Key
```

### Step 3: Commit and Push GitHub Actions

```powershell
git add .github/workflows/
git commit -m "Add GitHub Actions CI/CD"
git push origin Dev
```

### Step 4: Test the Workflow

1. Make a small change to any file
2. Commit and push to Dev:
   ```powershell
   git add .
   git commit -m "Test CI/CD"
   git push origin Dev
   ```
3. Go to GitHub → **Actions** tab
4. Watch the deployment happen automatically!

---

## How It Works

### Development Workflow
```
1. Make changes on Dev branch
2. Commit and push to GitHub
3. GitHub Actions automatically:
   - Builds backend
   - Deploys to dev-env on AWS
   - Builds frontend
   - Deploys to dev S3 bucket
4. Your dev site is updated!
```

### Production Workflow
```
1. Merge Dev into Prod branch
2. Push Prod to GitHub
3. GitHub Actions automatically:
   - Builds backend
   - Deploys to production-env on AWS
   - Builds frontend
   - Deploys to production S3 bucket
4. Your production site is updated!
```

---

## Workflow Files

### `.github/workflows/deploy-dev.yml`
- Triggers on push to **Dev** branch
- Deploys to **dev-env** and **dev S3 bucket**

### `.github/workflows/deploy-prod.yml`
- Triggers on push to **Prod** branch
- Deploys to **production-env** and **production S3 bucket**

---

## Benefits

✅ **Automatic Deployment** - No manual deployment needed
✅ **Consistent Process** - Same deployment every time
✅ **Fast** - Deploys in 3-5 minutes
✅ **Safe** - Dev and Prod are separate
✅ **Traceable** - See deployment history in GitHub Actions

---

## Monitoring Deployments

### View Deployment Status
1. Go to your GitHub repository
2. Click **Actions** tab
3. See all deployments and their status

### View Deployment Logs
1. Click on any deployment
2. Click on the job name
3. See detailed logs of each step

---

## Troubleshooting

### Deployment Failed
1. Go to GitHub Actions
2. Click the failed deployment
3. Check the error logs
4. Fix the issue and push again

### AWS Credentials Error
- Make sure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in GitHub Secrets
- Check that the credentials have proper permissions

### Build Error
- Check the logs in GitHub Actions
- Test the build locally first:
  ```powershell
  cd frontend
  npm run build
  ```

---

## Next Steps

1. **Add secrets to GitHub** (Step 1 above)
2. **Push the workflow files** (Step 3 above)
3. **Test with a small change** (Step 4 above)
4. **Enjoy automatic deployments!** 🎉

---

## Manual Deployment (Backup)

If GitHub Actions is down, you can still deploy manually:

```powershell
# Deploy to Dev
.\deploy-to-dev.ps1

# Deploy to Prod
.\deploy-to-prod.ps1
```

---

**Your deployment is now automated!** Every push to Dev or Prod will automatically deploy to AWS.
