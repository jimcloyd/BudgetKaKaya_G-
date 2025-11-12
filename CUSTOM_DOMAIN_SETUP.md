# Setting Up a Custom Domain

## Overview

Instead of:
- `budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com`

You can have:
- `budgettracker.com`
- `mybudget.com`
- `familybudget.app`
- Or any domain you want!

---

## Option 1: Buy a Domain (Recommended)

### Where to Buy
- **Namecheap** - $8-12/year - https://www.namecheap.com
- **GoDaddy** - $10-15/year - https://www.godaddy.com
- **Google Domains** - $12/year - https://domains.google
- **AWS Route 53** - $12/year - Built into AWS

### Recommended Domains
- `budgettracker.com`
- `familybudget.app`
- `mybudget.online`
- `budgetkakaya.com` (your project name!)

**Cost**: $8-15/year

---

## Option 2: Use a Free Subdomain

### Free Options
- **Freenom** - Free .tk, .ml, .ga domains
- **Afraid.org** - Free subdomains
- **No-IP** - Free dynamic DNS

**Note**: Free domains may look less professional

---

## Setup Steps (After Buying Domain)

### Step 1: Configure Domain in AWS Route 53

```powershell
# Create hosted zone
aws route53 create-hosted-zone --name budgettracker.com --caller-reference $(Get-Date -Format "yyyyMMddHHmmss")
```

### Step 2: Update Domain Nameservers

1. Go to your domain registrar (Namecheap, GoDaddy, etc.)
2. Find "Nameservers" or "DNS Settings"
3. Change to AWS nameservers (from Route 53):
   ```
   ns-1234.awsdns-12.org
   ns-5678.awsdns-34.com
   ns-9012.awsdns-56.net
   ns-3456.awsdns-78.co.uk
   ```
4. Save (takes 24-48 hours to propagate)

### Step 3: Create SSL Certificate (Free)

```powershell
# Request certificate
aws acm request-certificate `
    --domain-name budgettracker.com `
    --domain-name www.budgettracker.com `
    --validation-method DNS `
    --region us-east-1
```

### Step 4: Set Up CloudFront Distribution

```powershell
# Create CloudFront distribution for S3
aws cloudfront create-distribution `
    --origin-domain-name budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com `
    --default-root-object index.html
```

### Step 5: Point Domain to CloudFront

```powershell
# Create Route 53 record
aws route53 change-resource-record-sets `
    --hosted-zone-id YOUR_ZONE_ID `
    --change-batch file://dns-record.json
```

**dns-record.json**:
```json
{
  "Changes": [{
    "Action": "CREATE",
    "ResourceRecordSet": {
      "Name": "budgettracker.com",
      "Type": "A",
      "AliasTarget": {
        "HostedZoneId": "Z2FDTNDATAQYW2",
        "DNSName": "d1234567890.cloudfront.net",
        "EvaluateTargetHealth": false
      }
    }
  }]
}
```

---

## Quick Setup (Simplified)

### Using AWS Amplify (Easiest)

1. **Deploy to Amplify**
   ```powershell
   # Install Amplify CLI
   npm install -g @aws-amplify/cli
   
   # Initialize
   cd frontend
   amplify init
   
   # Add hosting
   amplify add hosting
   
   # Deploy
   amplify publish
   ```

2. **Add Custom Domain**
   - Go to Amplify Console
   - Click "Domain management"
   - Click "Add domain"
   - Enter your domain
   - Follow verification steps
   - Done! (Amplify handles SSL automatically)

**Benefits**:
- ✅ Automatic SSL
- ✅ CDN included
- ✅ Easy domain setup
- ✅ Continuous deployment

---

## Cost Breakdown

### Domain Only
- **Domain**: $8-15/year
- **AWS Route 53**: $0.50/month
- **SSL Certificate**: FREE (AWS Certificate Manager)
- **CloudFront**: ~$1-5/month (based on traffic)

**Total**: ~$20-30/year

### With Amplify
- **Domain**: $8-15/year
- **Amplify Hosting**: FREE tier (1000 build minutes/month)
- **SSL**: FREE (automatic)

**Total**: ~$8-15/year

---

## Recommended Domain Names

Based on your project:

1. **budgetkakaya.com** - Matches your GitHub repo
2. **familybudget.app** - Clear purpose
3. **mybudgettracker.com** - Professional
4. **budgetko.com** - Short and catchy (Filipino touch)
5. **kakayabudget.com** - Unique

Check availability: https://www.namecheap.com

---

## Quick Start Guide

### For Beginners (Easiest)

1. **Buy domain** at Namecheap ($10/year)
2. **Use Cloudflare** (Free CDN + SSL)
   - Add site to Cloudflare
   - Point to your S3 bucket
   - Get free SSL automatically
3. **Done!** Your app is at your custom domain

### For AWS Users

1. **Buy domain** anywhere
2. **Use Route 53** for DNS
3. **Use CloudFront** for CDN + SSL
4. **Use Certificate Manager** for free SSL
5. **Done!** Professional setup

---

## Step-by-Step: Cloudflare Method (Easiest + Free SSL)

### Step 1: Buy Domain
- Go to Namecheap
- Search for domain
- Buy it ($8-12/year)

### Step 2: Add to Cloudflare
1. Go to https://www.cloudflare.com
2. Sign up (free)
3. Click "Add a Site"
4. Enter your domain
5. Choose Free plan
6. Cloudflare scans your DNS

### Step 3: Update Nameservers
1. Cloudflare gives you 2 nameservers
2. Go to Namecheap
3. Change nameservers to Cloudflare's
4. Wait 24 hours

### Step 4: Add DNS Record
In Cloudflare:
1. Go to DNS settings
2. Add CNAME record:
   - **Name**: `@` (or `www`)
   - **Target**: `budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com`
   - **Proxy**: ON (orange cloud)
3. Save

### Step 5: Enable SSL
In Cloudflare:
1. Go to SSL/TLS
2. Choose "Flexible"
3. Done! SSL is automatic

**Result**: Your app is now at `yourdomain.com` with HTTPS! 🎉

---

## Benefits of Custom Domain

✅ **Professional** - Looks more trustworthy  
✅ **Memorable** - Easy to share with your wife  
✅ **Branding** - Your own identity  
✅ **SSL/HTTPS** - Secure connection  
✅ **SEO** - Better for search engines  

---

## Recommendations

### For Personal Use (You + Wife)
- **Option**: Cloudflare method
- **Cost**: $10/year (domain only)
- **Time**: 1 hour setup
- **Benefit**: Free SSL, easy setup

### For Professional Use
- **Option**: AWS Route 53 + CloudFront
- **Cost**: $30/year
- **Time**: 2 hours setup
- **Benefit**: Full AWS integration

### For Future Growth
- **Option**: AWS Amplify
- **Cost**: $15/year
- **Time**: 30 minutes setup
- **Benefit**: Automatic deployments, scaling

---

## My Recommendation

**Start with Cloudflare method**:
1. Buy `budgetkakaya.com` on Namecheap ($10)
2. Set up Cloudflare (free)
3. Get free SSL automatically
4. Total cost: $10/year
5. Setup time: 1 hour

Later, you can always migrate to full AWS setup if needed.

---

## Need Help?

I can help you:
1. Choose a domain name
2. Set up DNS records
3. Configure SSL
4. Test the setup

Just let me know what domain you want! 🌐

---

**Current URL**: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com  
**Future URL**: https://yourdomain.com

Much better! 🚀
