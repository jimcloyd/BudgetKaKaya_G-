# Configure AWS CLI

## Step 1: Run AWS Configure

Open your terminal and run:

```powershell
aws configure
```

## Step 2: Enter Your Credentials

You'll be prompted for 4 pieces of information:

### 1. AWS Access Key ID
```
AWS Access Key ID [None]: 
```
**Enter your NEW Access Key ID** (starts with AKIA...)

⚠️ **Important**: Use NEW credentials, not the ones posted earlier!

### 2. AWS Secret Access Key
```
AWS Secret Access Key [None]: 
```
**Enter your NEW Secret Access Key**

### 3. Default Region
```
Default region name [None]: us-east-1
```
**Type**: `us-east-1` (recommended for beginners)

### 4. Default Output Format
```
Default output format [None]: json
```
**Type**: `json`

## Step 3: Verify Configuration

After configuration, test it:

```powershell
aws sts get-caller-identity
```

**Expected output:**
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

If you see this, you're all set! ✅

## Troubleshooting

### If you get "command not found"
Close and reopen your terminal, then try again.

### If you get "Invalid credentials"
- Make sure you copied the credentials correctly
- Check that you're using NEW credentials (not the exposed ones)
- Verify the credentials in AWS Console → Security credentials

### If you need to reconfigure
Just run `aws configure` again - it will overwrite the previous configuration.

## Where Are Credentials Stored?

Your credentials are stored locally at:
```
C:\Users\YourUsername\.aws\credentials
```

This file is **local only** and should never be shared or committed to Git.

## Next Steps

Once configured successfully:
1. ✅ AWS CLI is configured
2. ✅ Ready to deploy to AWS
3. ✅ Continue with deployment guide

Open `AWS_GETTING_STARTED.md` and jump to **Step 3: Choose Your Deployment Strategy**!
