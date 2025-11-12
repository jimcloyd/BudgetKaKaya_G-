#!/bin/bash

# Deploy Backend to AWS Elastic Beanstalk
# Usage: ./deploy-backend.sh

set -e

echo "=========================================="
echo "Deploying Backend to AWS Elastic Beanstalk"
echo "=========================================="

cd backend

# Check if EB is initialized
if [ ! -d ".elasticbeanstalk" ]; then
    echo "Error: Elastic Beanstalk not initialized."
    echo "Please run: eb init -p python-3.9 family-budget-tracker --region us-east-1"
    exit 1
fi

# Check if environment exists
if ! eb status > /dev/null 2>&1; then
    echo "Error: No EB environment found."
    echo "Please create an environment first."
    exit 1
fi

echo "Deploying application..."
eb deploy

echo ""
echo "Deployment complete!"
echo "Check status with: eb status"
echo "View logs with: eb logs"
echo ""
echo "Don't forget to run database migrations if needed:"
echo "  eb ssh"
echo "  source /var/app/venv/*/bin/activate"
echo "  cd /var/app/current"
echo "  flask db upgrade"
