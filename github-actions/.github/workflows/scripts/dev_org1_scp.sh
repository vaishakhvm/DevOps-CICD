#!/bin/bash
# ============================================================================
# Org1 UI Environment File Transfer Script for DEV (Enhanced)
# ============================================================================
set -euo pipefail  # Exit on error, undefined vars, and pipe failures

# ----------------------------------------------------------------------------
# Configuration Variables
# ----------------------------------------------------------------------------
SSH_KEY="/datadisk/sshkey/key-pair.pem"
REMOTE_USER="<username>"
REMOTE_HOST="<IP>"
REMOTE_PATH="/home/ubuntu/Org1/react-ui"
LOCAL_PATH="/datadisk/org1/react-ui"
ENV_FILE="ui.env.dev"

# ----------------------------------------------------------------------------
# Step 1: Display Current Working Directory
# Helps with debugging and log traceability
# ----------------------------------------------------------------------------
echo "📍 Current directory:"
pwd

# ----------------------------------------------------------------------------
# Step 2: Create Remote Backup via SSH
# Backup existing .env.dev to .env.dev.rb (rollback file)
# ----------------------------------------------------------------------------
echo "💾 Creating backup of existing .env.dev on remote server..."
ssh -o StrictHostKeyChecking=no \
    -i "${SSH_KEY}" \
    ${REMOTE_USER}@${REMOTE_HOST} \
    "cd ${REMOTE_PATH} && cp .env.dev .env.dev.rb && echo '✅ Backup created: .env.dev.rb'"

# ----------------------------------------------------------------------------
# Step 3: Navigate to Local Directory
# Ensure we're in the correct directory containing source files
# ----------------------------------------------------------------------------
echo "📂 Changing to local directory: ${LOCAL_PATH}"
cd ${LOCAL_PATH}

# ----------------------------------------------------------------------------
# Step 4: Verify Local File Exists Before Transfer
# Prevents SCP failure if source file is missing
# ----------------------------------------------------------------------------
if [ ! -f "${ENV_FILE}" ]; then
    echo "❌ Error: Local file ${ENV_FILE} not found in ${LOCAL_PATH}"
    exit 1
fi

echo "✅ Local file found: ${ENV_FILE}"

# ----------------------------------------------------------------------------
# Step 5: Transfer Updated Environment File to Remote Server
# Securely copy .env file using SCP over SSH
# ----------------------------------------------------------------------------
echo "📤 Transferring ${ENV_FILE} to remote server..."
scp -o StrictHostKeyChecking=no \
    -i '/datadisk/sshkey/ace-key-pair.pem' \
    ${LOCAL_PATH}/${ENV_FILE} \
    ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

echo "✅ File transfer completed successfully"

# ----------------------------------------------------------------------------
# Step 6: Verify Remote File Exists After Transfer
# Confirm file was successfully copied to remote server
# ----------------------------------------------------------------------------
echo "🔍 Verifying file on remote server..."
ssh -o StrictHostKeyChecking=no \
    -i "${SSH_KEY}" \
    ${REMOTE_USER}@${REMOTE_HOST} \
    "ls -lh ${REMOTE_PATH}/${ENV_FILE}"

echo "🎉 Environment file transfer and verification complete!"

# Exit with success
exit 0
