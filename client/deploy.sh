#!/bin/bash

# Build the React app
echo "Building the React app..."
npm run build

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo "Build failed. Aborting deployment."
    exit 1
fi

# Set your S3 bucket name
S3_BUCKET="your-s3-bucket-name"

# Upload the build folder to S3
echo "Uploading build to S3..."
aws s3 sync build/ s3://$S3_BUCKET --delete

# Check if the upload was successful
if [ $? -eq 0 ]; then
    echo "Deployment successful! Your app is now live on S3."
    echo "Your app is available at: http://$S3_BUCKET.s3-website-us-east-1.amazonaws.com"
else
    echo "Deployment failed. Please check your AWS credentials and S3 bucket permissions."
    exit 1
fi
