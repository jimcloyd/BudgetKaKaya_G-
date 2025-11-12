#!/bin/bash

# Deploy Frontend to AWS S3 + CloudFront
# Usage: ./deploy-frontend.sh <s3-bucket-name> <cloudfront-distribution-id>

set -e

if [ -z "$1" ]; then
    echo "Error: S3 bucket name required"
    echo "Usage: ./deploy-frontend.sh <s3-bucket-name> [cloudfront-distribution-id]"
    exit 1
fi

S3_BUCKET=$1
CLOUDFRONT_ID=$2

echo "=========================================="
echo "Deploying Frontend to AWS S3"
echo "=========================================="

cd frontend

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo "Warning: .env.production not found"
    echo "Creating template .env.production file..."
    echo "VITE_API_URL=https://your-api-url.com/api" > .env.production
    echo "Please update .env.production with your actual API URL"
    exit 1
fi

echo "Building frontend..."
npm run build

echo "Uploading to S3..."
aws s3 sync dist/ s3://$S3_BUCKET --delete

echo "Frontend deployed to S3!"

if [ ! -z "$CLOUDFRONT_ID" ]; then
    echo "Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id $CLOUDFRONT_ID \
        --paths "/*"
    echo "CloudFront cache invalidated!"
fi

echo ""
echo "Deployment complete!"
echo "S3 Bucket: s3://$S3_BUCKET"
if [ ! -z "$CLOUDFRONT_ID" ]; then
    echo "CloudFront Distribution: $CLOUDFRONT_ID"
fi
