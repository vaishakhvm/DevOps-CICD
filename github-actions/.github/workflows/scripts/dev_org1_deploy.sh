#!/bin/bash
# ============================================================================
# Org1 UI Deployment Script for DEV Environment
# ============================================================================
# Purpose: Deploy Org1 React UI to the DEV server via SSH
# 
# What this script does:
# 1. SSH into the remote DEV server
# 2. Stop existing Docker containers
# 3. Pull the latest Docker image
# 4. Start updated containers
# 5. Verify deployment success
#
# Usage: bash dev_org1_deploy.sh
# Called by: GitHub Actions workflow (Deploy Org1 UI to DEV)
# ============================================================================

# ----------------------------------------------------------------------------
# Error Handling Configuration
# ----------------------------------------------------------------------------
# set -e: Exit immediately if any command fails
# set -u: Treat unset variables as errors
# set -o pipefail: Catch errors in piped commands
# These flags ensure script fails fast on any error
# ----------------------------------------------------------------------------
set -euo pipefail

# ============================================================================
# SSH Connection & Remote Execution
# ============================================================================
# SSH Options:
#   -o StrictHostKeyChecking=no : Auto-accept new host keys (for automation)
#   -i : Specify private key file for authentication
#
# Heredoc (<<'EOF'...EOF):
#   Sends all commands between EOF markers to remote server
#   Quotes around 'EOF' prevent local variable expansion
#   Commands execute on remote server, not locally
# ============================================================================
ssh -o StrictHostKeyChecking=no \
    -i '/datadisk/sshkey/key-pair.pem' \
    <Username>@<IP> << 'EOF'

# ----------------------------------------------------------------------------
# Remote Server Error Handling
# Apply same strict error handling on remote server
# ----------------------------------------------------------------------------
set -euo pipefail

# ----------------------------------------------------------------------------
# Step 1: Navigate to Application Directory
# Location: /datadisk/org1/react-ui (contains docker-compose.yml)
# ----------------------------------------------------------------------------
cd /datadisk/org1/react-ui

# ----------------------------------------------------------------------------
# Step 2: Pre-Deployment Health Check
# Check available disk space to ensure sufficient storage for deployment
# Displays filesystem usage for root partition
# ----------------------------------------------------------------------------
echo "🔍 Checking disk space..."
df -h /

# ----------------------------------------------------------------------------
# Step 3: Stop Existing Containers
# Gracefully stops and removes containers defined in docker-compose.yml
# Uses .env.dev for environment-specific configuration
# 
# docker compose down:
#   - Stops running containers
#   - Removes containers, networks, volumes (optional)
#   - Preserves images for faster restart
# ----------------------------------------------------------------------------
echo "🛑 Stopping existing containers..."
docker compose --env-file /datadisk/org1/react-ui/.env.dev down

# ----------------------------------------------------------------------------
# Step 4: Pull Latest Docker Image
# Downloads the newest version of the image from Docker registry
# Version is specified in .env.dev file (service_version variable)
# 
# docker compose pull:
#   - Fetches image tagged with version from .env.dev
#   - Does not affect running containers (already stopped)
#   - May take time depending on image size and network speed
# ----------------------------------------------------------------------------
echo "📥 Pulling new image..."
docker compose --env-file /datadisk/org1/react-ui/.env.dev pull

# ----------------------------------------------------------------------------
# Step 5: Start Updated Containers
# Launches containers using the newly pulled image
# 
# docker compose up -d:
#   -d (detached mode): Runs containers in background
#   Uses configuration from docker-compose.yml + .env.dev
#   Creates networks, volumes if needed
# ----------------------------------------------------------------------------
echo "🚀 Starting containers..."
docker compose --env-file /datadisk/org1/react-ui/.env.dev up -d

# ----------------------------------------------------------------------------
# Step 6: Wait for Container Initialization
# Give containers time to fully start and initialize
# 5 seconds is usually sufficient for basic health checks
# Adjust if containers need more startup time
# ----------------------------------------------------------------------------
echo "⏳ Waiting for containers..."
sleep 5

# ----------------------------------------------------------------------------
# Step 7: Display Container Status
# Shows current state of all containers managed by docker-compose
# Useful for quick visual verification in logs
# 
# Output includes: Name, Status, Ports, etc.
# ----------------------------------------------------------------------------
echo "📊 Container status:"
docker compose ps

# ----------------------------------------------------------------------------
# Step 8: Verify Specific Container Exists
# Checks if the org1-dev-ui container was created successfully
# 
# docker inspect:
#   Returns detailed container information
#   Redirects output to /dev/null (we only care about exit code)
#   Exit code 0 = container exists, non-zero = doesn't exist
# ----------------------------------------------------------------------------
echo "🧪 Verifying org1-dev-ui is running..."
if ! docker inspect org1-dev-ui >/dev/null 2>&1; then
  echo "❌ Container org1-dev-ui does not exist"
  # Display all containers (including stopped ones) for debugging
  docker ps -a
  exit 1
fi

# ----------------------------------------------------------------------------
# Step 9: Verify Container is Actually Running
# Confirms that org1-dev-ui container is not just created, but actively running
# 
# docker inspect -f '{{.State.Running}}':
#   -f : Format output using Go template
#   {{.State.Running}} : Returns "true" or "false"
#   
# Possible states: running, restarting, paused, exited
# ----------------------------------------------------------------------------
if [ "$(docker inspect -f '{{.State.Running}}' org1-dev-ui)" != "true" ]; then
  echo "❌ Container org1-dev-ui is NOT running"
  # Display all containers for debugging
  docker ps -a
  exit 1
fi

# ----------------------------------------------------------------------------
# Step 10: Success Confirmation
# All checks passed - deployment completed successfully
# ----------------------------------------------------------------------------
echo "✅ org1-dev-ui container is running"
echo "🎉 Deployment successful!"

# ============================================================================
# End of Remote Execution Block
# ============================================================================
EOF

# ============================================================================
# Script Exit
# If we reach here, SSH session completed successfully
# GitHub Actions will mark this step as passed
# ============================================================================
