# OpenShift Deployment Guide

## Overview
This directory contains all YAML files needed to deploy the Tweet Processing API to OpenShift.

## Files Structure
```
infra/
├── secret.yaml          # MongoDB credentials
├── configmap.yaml       # Application configuration
├── deployment.yaml      # Application deployment
├── service.yaml         # Internal service
├── route.yaml          # External route (OpenShift specific)
├── kustomization.yaml  # Kustomize configuration
└── README.md           # This file
```

## Deployment Steps

### Method 1: Using Kustomize (Recommended)
```bash
# Apply all resources at once
oc apply -k infra/

# Check deployment status
oc get pods -l app=tweet-processor
oc get svc tweet-processor-service
oc get route tweet-processor-route
```

### Method 2: Apply Each File Individually
```bash
# Apply in this order
oc apply -f infra/secret.yaml
oc apply -f infra/configmap.yaml
oc apply -f infra/deployment.yaml
oc apply -f infra/service.yaml
oc apply -f infra/route.yaml
```

## Verification

### Check Pod Status
```bash
oc get pods -l app=tweet-processor
oc describe pod <pod-name>
oc logs <pod-name>
```

### Check Service
```bash
oc get svc tweet-processor-service
oc describe svc tweet-processor-service
```

### Check Route
```bash
oc get route tweet-processor-route
oc describe route tweet-processor-route
```

### Test API
```bash
# Get the route URL
ROUTE_URL=$(oc get route tweet-processor-route -o jsonpath='{.spec.host}')

# Test health endpoint
curl https://$ROUTE_URL/

# Test main API endpoint
curl https://$ROUTE_URL/api/processed-tweets
```

## Environment Variables

The application uses the following environment variables from the secret:

- `USER`: MongoDB username
- `MONGO_PASSWORD`: MongoDB password  
- `MONGO_DB_NAME`: MongoDB database name
- `MONGO_CONNECTION_STRING`: Full MongoDB connection string
- `MONGODB_COLLECTION`: MongoDB collection name

## Scaling

### Scale Up/Down
```bash
# Scale to 3 replicas
oc scale deployment tweet-processor-api --replicas=3

# Scale down to 1 replica
oc scale deployment tweet-processor-api --replicas=1
```

## Troubleshooting

### Common Issues

1. **Pod fails to start**
   ```bash
   oc describe pod <pod-name>
   oc logs <pod-name>
   ```

2. **Database connection issues**
   - Check secret values are correct
   - Verify MongoDB connection string
   - Check network connectivity

3. **Route not accessible**
   ```bash
   oc get route
   oc describe route tweet-processor-route
   ```

### Useful Commands
```bash
# Check all resources
oc get all -l app=tweet-processor

# Delete all resources
oc delete -k infra/

# View logs
oc logs -f deployment/tweet-processor-api

# Execute into pod
oc exec -it <pod-name> -- /bin/bash
```

## Resource Limits

Current configuration:
- **Requests**: 256Mi memory, 100m CPU
- **Limits**: 512Mi memory, 500m CPU

Adjust in `deployment.yaml` if needed based on load testing.

## Security Notes

- Credentials are stored in OpenShift secrets (base64 encoded)
- TLS termination is enabled on the route
- HTTP traffic is redirected to HTTPS
