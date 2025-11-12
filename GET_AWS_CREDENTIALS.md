# How to Get Your AWS Credentials

## Option 1: Check Your Existing Credentials (Recommended)

Your AWS credentials are stored locally. Let's retrieve them:

### On Windows:

```powershell
# View your credentials file
notepad $env:USERPROFILE\.aws\credentials
```

This will open a file that looks like:
```
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Copy these values:**
- `aws_access_key_id` → This is your **AWS_ACCESS_KEY_ID**
- `aws_secret_access_key` → This is your **AWS_SECRET_ACCESS_KEY**

---

## Option 2: Create New Access Keys (If Needed)

If you don't have credentials or want new ones:

### Step 1: Go to AWS IAM Console
Open: https://console.aws.amazon.com/iam/

### Step 2: Navigate to Security Credentials
1. Click your username in the top right
2. Click **Security credentials**

### Step 3: Create Access Key
1. Scroll down to **Access keys**
2. Click **Create access key**
3. Select **Command Line Interface (CLI)**
4. Check the confirmation box
5. Click **Next**
6. (Optional) Add a description tag
7. Click **Create access key**

### Step 4: Save Your Credentials
⚠️ **IMPORTANT:** This is the ONLY time you'll see the secret key!

You'll see:
- **Access key ID**: `AKIAIOSFODNN7EXAMPLE`
- **Secret access key**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

**Save these somewhere safe!**

---

## Add to GitHub Secrets

Once you have your credentials:

### Step 1: Go to GitHub Repository Settings
https://github.com/jimcloyd/BudgetKaKaya_G-/settings/secrets/actions

### Step 2: Add AWS_ACCESS_KEY_ID
1. Click **New repository secret**
2. Name: `AWS_ACCESS_KEY_ID`
3. Value: Paste your access key ID (e.g., `AKIAIOSFODNN7EXAMPLE`)
4. Click **Add secret**

### Step 3: Add AWS_SECRET_ACCESS_KEY
1. Click **New repository secret**
2. Name: `AWS_SECRET_ACCESS_KEY`
3. Value: Paste your secret access key (e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)
4. Click **Add secret**

---

## Quick Command to View Credentials

```powershell
# Windows
Get-Content $env:USERPROFILE\.aws\credentials

# Or open in notepad
notepad $env:USERPROFILE\.aws\credentials
```

---

## Security Tips

✅ **DO:**
- Keep credentials secret
- Use GitHub Secrets for CI/CD
- Rotate keys periodically

❌ **DON'T:**
- Commit credentials to Git
- Share credentials publicly
- Use root account keys (use IAM user instead)

---

## Verify It Works

After adding to GitHub Secrets:

1. Go to your repository
2. Click **Actions** tab
3. Make a small change and push to Dev
4. Watch the deployment run automatically!

---

## Troubleshooting

### Can't find credentials file?
Run this to check if it exists:
```powershell
Test-Path $env:USERPROFILE\.aws\credentials
```

If it returns `False`, you need to create new access keys (Option 2 above).

### Credentials don't work?
- Make sure you copied the entire key (no spaces)
- Check that the IAM user has proper permissions
- Try creating new access keys

---

**Next:** After adding credentials to GitHub, your deployments will run automatically! 🚀
