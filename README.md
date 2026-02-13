# DevOps CI/CD Pipeline for Multi-Environment Deployments

[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?logo=gnu-bash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Semantic Versioning](https://img.shields.io/badge/Versioning-Semantic-informational)](https://semver.org/)

> **Enterprise-grade automated deployment pipeline for React UI applications across DEV, STG, UAT, and PROD environments with intelligent semantic versioning and Docker containerization.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Repository Structure](#-repository-structure)
- [Prerequisites](#-prerequisites)
- [Workflows](#-workflows)
  - [Multi-Stage Docker Build](#1-multi-stage-docker-build)
  - [Environment-Specific Deployment](#2-environment-specific-deployment)
- [Semantic Versioning System](#-semantic-versioning-system)
- [Deployment Scripts](#-deployment-scripts)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Troubleshooting](#-troubleshooting)
- [Security Best Practices](#-security-best-practices)
- [Contributing](#-contributing)

---

## 🎯 Overview

This repository implements a complete **CI/CD pipeline** for deploying containerized React applications across multiple environments. The pipeline automates the entire deployment lifecycle from building Docker images to deploying and verifying containers on remote servers.

### Key Capabilities

- ✅ **Multi-Environment Support**: DEV, STG, UAT, and PROD
- ✅ **Intelligent Versioning**: Auto-rollover semantic versioning (MAJOR.MINOR.PATCH)
- ✅ **Docker Containerization**: Secure, isolated deployments
- ✅ **Automated Workflows**: GitHub Actions-powered CI/CD
- ✅ **Security Scanning**: Container vulnerability detection
- ✅ **Safe Deployments**: Automatic backups and rollback capability
- ✅ **Health Checks**: Post-deployment verification
- ✅ **Audit Trail**: Comprehensive logging and summaries

---

## ✨ Features

### 🚀 Automated Build Pipeline
- **Multi-stage Docker builds** with environment-specific configurations
- **Vulnerability scanning** using container security tools
- **Automatic version bumping** (patch, minor, major)
- **Docker registry integration** with automated push
- **Build artifact management** with proper cleanup

### 📦 Deployment Automation
- **SSH-based secure deployments** to remote servers
- **Environment file management** with backup/rollback
- **Docker Compose orchestration** for service management
- **Container health verification** post-deployment
- **Zero-downtime deployments** with graceful restarts

### 🔢 Smart Version Management
- **Semantic versioning** (vMAJOR.MINOR.PATCH)
- **Auto-rollover logic**:
  - PATCH > 10 → rolls to MINOR (v1.0.11 → v1.1.0)
  - MINOR > 10 → rolls to MAJOR (v1.11.0 → v2.0.0)
- **Environment-specific version tracking**
- **Version persistence** in `.env` files

### 🔐 Security & Compliance
- **SSH key-based authentication** (no password storage)
- **Encrypted file transfers** via SCP
- **Secret management** through GitHub Secrets
- **Container security scanning** before deployment
- **Automated backup creation** before updates

---

## 🏗️ Architecture

### CI/CD Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DEVELOPER WORKFLOW                           │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Manual Trigger (workflow_dispatch)
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   MULTI-STAGE DOCKER BUILD WORKFLOW                  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  1. Environment Selection (dev/stg/uat/prod)                  │  │
│  │  2. Checkout Frontend Repository                              │  │
│  │  3. Copy Environment-Specific .env File                       │  │
│  │  4. Build Docker Image                                        │  │
│  │  5. Security Scan (Vulnerability Detection)                   │  │
│  │  6. Semantic Version Bump (patch/minor/major)                 │  │
│  │  7. Tag Image with New Version                                │  │
│  │  8. Push to Docker Registry                                   │  │
│  │  9. Trigger Environment-Specific Deployment                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Workflow Dispatch
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              ENVIRONMENT-SPECIFIC DEPLOYMENT WORKFLOW                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  1. Checkout Deployment Scripts                               │  │
│  │  2. Display Deployment Information                            │  │
│  │  3. SCP Transfer: Copy .env to Remote Server                  │  │
│  │     ├─ Create Backup (.env.dev.rb)                            │  │
│  │     └─ Transfer Updated .env File                             │  │
│  │  4. SSH Deployment: Execute on Remote Server                  │  │
│  │     ├─ Stop Existing Containers                               │  │
│  │     ├─ Pull New Docker Image                                  │  │
│  │     ├─ Start Updated Containers                               │  │
│  │     ├─ Wait for Initialization                                │  │
│  │     └─ Verify Container Health                                │  │
│  │  5. Generate Deployment Summary                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DEPLOYED APPLICATION                            │
│                   Running on Remote Server                           │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Interaction

```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  GitHub Actions  │────────▶│  Python Script   │────────▶│  .env Files      │
│   Workflows      │         │   (pyver.py)     │         │  (Versioning)    │
└──────────────────┘         └──────────────────┘         └──────────────────┘
        │                              │
        │                              ▼
        │                    ┌──────────────────┐
        │                    │  Docker Registry │
        │                    │  (Image Storage) │
        │                    └──────────────────┘
        │
        ▼
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  Bash Scripts    │────────▶│  SSH/SCP         │────────▶│  Remote Server   │
│  (Deployment)    │         │  (Secure Copy)   │         │  (Target Env)    │
└──────────────────┘         └──────────────────┘         └──────────────────┘
        │
        ▼
┌──────────────────┐
│  Docker Compose  │
│  (Orchestration) │
└──────────────────┘
```

---

## 📁 Repository Structure

```
DevOps-CICD/
├── .github/
│   └── workflows/
│       ├── mulit-stage-docker-build.yml    # Main build & version workflow
│       ├── deploy_org1-dev.yml             # DEV deployment workflow
│       ├── deploy_org1-stg.yml             # STG deployment workflow (similar)
│       ├── deploy_org1-uat.yml             # UAT deployment workflow (similar)
│       ├── deploy_org1-prod.yml            # PROD deployment workflow (similar)
│       └── scripts/
│           ├── pyver.py                    # Semantic versioning script
│           ├── dev_org1_scp.sh             # Environment file transfer (DEV)
│           ├── dev_org1_deploy.sh          # Deployment execution (DEV)
│           ├── stg_org1_scp.sh             # Environment file transfer (STG)
│           ├── stg_org1_deploy.sh          # Deployment execution (STG)
│           ├── uat_org1_scp.sh             # Environment file transfer (UAT)
│           ├── uat_org1_deploy.sh          # Deployment execution (UAT)
│           ├── prod_org1_scp.sh            # Environment file transfer (PROD)
│           └── prod_org1_deploy.sh         # Deployment execution (PROD)
├── .env.dev                                # DEV environment versions
├── .env.stg                                # STG environment versions
├── .env.uat                                # UAT environment versions
├── .env.prod                               # PROD environment versions
└── README.md                               # This file
```

---

## 🔧 Prerequisites

### Required Software & Tools

| Tool | Version | Purpose |
|------|---------|---------|
| **GitHub Actions Runner** | Self-hosted | CI/CD execution environment |
| **Docker** | 20.10+ | Container runtime |
| **Docker Compose** | 2.x | Multi-container orchestration |
| **Python** | 3.10+ | Version management script |
| **Bash** | 4.0+ | Deployment scripts |
| **SSH** | OpenSSH | Secure remote connections |
| **SCP** | OpenSSH | Secure file transfers |

### Python Dependencies

```bash
pip install python-dotenv semantic_version
```

### GitHub Secrets Configuration

Configure the following secrets in your GitHub repository:

```
REGISTRY_NAME       # Docker registry URL (e.g., registry.example.com)
DOCKER_USERNAME     # Docker registry username
DOCKER_PASSWORD     # Docker registry password/token
```

### SSH Key Setup

1. **Generate SSH key pair** (if not exists):
   ```bash
   ssh-keygen -t rsa -b 4096 -f /path/to/key-pair.pem
   ```

2. **Copy public key to remote servers**:
   ```bash
   ssh-copy-id -i /path/to/key-pair.pem.pub user@remote-server
   ```

3. **Set proper permissions**:
   ```bash
   chmod 600 /path/to/key-pair.pem
   ```

---

## 🔄 Workflows

### 1. Multi-Stage Docker Build

**File**: `.github/workflows/mulit-stage-docker-build.yml`

#### Purpose
Builds Docker images for React UI applications with environment-specific configurations, performs security scanning, manages semantic versioning, and triggers environment-specific deployments.

#### Trigger
Manual workflow dispatch via GitHub Actions UI

#### Inputs

| Parameter | Type | Options | Description |
|-----------|------|---------|-------------|
| `environment` | Choice | dev, stg, uat, prod | Target deployment environment |
| `version_type` | Choice | patch, minor, major | Semantic version increment type |

#### Workflow Steps

1. **Checkout Frontend Repository**
   - Fetches source code with shallow clone

2. **Python Setup & Dependencies**
   - Installs Python 3.10
   - Installs `python-dotenv` and `semantic_version`

3. **Environment Configuration**
   - Maps environment to appropriate `.env` file path
   - Copies environment-specific configuration

4. **Docker Registry Authentication**
   - Logs into Docker registry using secrets

5. **Docker Image Build**
   - Builds container image with environment context
   - Tags with temporary label

6. **Security Vulnerability Scan**
   - Scans image for CRITICAL vulnerabilities
   - Continues on non-critical findings

7. **Semantic Version Update**
   - Reads current version from `.env` file
   - Increments version based on `version_type`
   - Updates `.env` file with new version

8. **Image Tagging & Push**
   - Tags image with semantic version
   - Pushes to Docker registry
   - Cleans up temporary images

9. **Trigger Deployment**
   - Automatically triggers environment-specific deployment workflow
   - Passes environment and version as inputs

#### Example Usage

```yaml
# Trigger via GitHub Actions UI
Environment: dev
Version Type: patch

# Result
Current Version: v1.2.5
New Version: v1.2.6
Image: registry.example.com/react-ui-dev:v1.2.6
```

---

### 2. Environment-Specific Deployment

**File**: `.github/workflows/deploy_org1-dev.yml` (example for DEV)

#### Purpose
Deploys a specific version of the Docker image to the target environment server, handles environment file transfer, and verifies successful deployment.

#### Trigger
- Manual workflow dispatch
- Automatically triggered by build workflow

#### Inputs

| Parameter | Type | Description |
|-----------|------|-------------|
| `environment` | String | Target environment (must match 'dev') |
| `version` | String | Docker image version tag to deploy |

#### Workflow Steps

1. **Checkout Repository**
   - Clones deployment scripts

2. **Display Deployment Info**
   - Logs version, environment, and trigger details

3. **Environment File Transfer**
   - Executes `dev_org1_scp.sh`
   - Creates backup of existing `.env` on remote server
   - Transfers updated `.env` file via SCP

4. **Docker Deployment**
   - Executes `dev_org1_deploy.sh`
   - Stops existing containers
   - Pulls new Docker image
   - Starts updated containers
   - Verifies container health

5. **Deployment Summary**
   - Generates success/failure summary
   - Logs timestamp and actor

#### Safety Features

- Environment validation (prevents wrong environment deployments)
- Automatic rollback capability via `.env.rb` backup
- Container health verification
- Fail-fast error handling

---

## 🔢 Semantic Versioning System

### Version Management Script

**File**: `.github/workflows/scripts/pyver.py`

#### Overview
Python script that manages semantic versioning across multiple environments with intelligent auto-rollover logic.

#### Version Format
```
vMAJOR.MINOR.PATCH
```
- **MAJOR**: Breaking changes, incompatible API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, minor improvements

#### Auto-Rollover Logic

```python
# Patch Rollover
v1.0.9  → v1.0.10  (normal increment)
v1.0.10 → v1.1.0   (patch > 10, rolls to minor)

# Minor Rollover
v1.9.5  → v1.10.5  (normal increment)
v1.10.5 → v1.11.5  (normal increment)
v1.10.10 → v2.0.0  (minor > 10, rolls to major)
```

#### Usage

```bash
python pyver.py <version_type> <environment> <base_path>

# Examples
python pyver.py patch dev /app           # Increment patch version
python pyver.py minor stg /app           # Increment minor version
python pyver.py major prod /app          # Increment major version
python pyver.py auto uat /app            # Auto-increment with rollover
```

#### Version Types

| Type | Behavior | Example |
|------|----------|---------|
| `patch` | Increment PATCH with rollover | 1.2.3 → 1.2.4 |
| `minor` | Increment MINOR, reset PATCH | 1.2.3 → 1.3.0 |
| `major` | Increment MAJOR, reset all | 1.2.3 → 2.0.0 |
| `auto` | Same as patch with rollover | 1.0.10 → 1.1.0 |

#### Environment Files

Each environment maintains its own version:

```bash
/path/to/.env.dev   # service_version=v1.2.6
/path/to/.env.stg   # service_version=v1.2.5
/path/to/.env.uat   # service_version=v1.2.3
/path/to/.env.prod  # service_version=v1.2.0
```

---

## 📜 Deployment Scripts

### Environment File Transfer Script

**File**: `.github/workflows/scripts/dev_org1_scp.sh`

#### Purpose
Securely transfers environment configuration files to remote servers with backup creation.

#### Operations

1. **Display Current Directory**
   - Logs execution context for debugging

2. **Create Remote Backup**
   ```bash
   # Creates rollback file
   .env.dev → .env.dev.rb
   ```

3. **Local File Validation**
   - Verifies source file exists before transfer

4. **Secure File Transfer**
   - Uses SCP over SSH
   - Transfers `ui.env.dev` to remote server

5. **Remote Verification**
   - Confirms successful file transfer

#### Script Structure

```bash
#!/bin/bash
set -euo pipefail  # Strict error handling

# Configuration
SSH_KEY="/datadisk/sshkey/key-pair.pem"
REMOTE_USER="<username>"
REMOTE_HOST="<IP>"
REMOTE_PATH="/home/ubuntu/Org1/react-ui"
LOCAL_PATH="/datadisk/org1/react-ui"
ENV_FILE="ui.env.dev"

# 1. Backup remote .env
ssh ... "cp .env.dev .env.dev.rb"

# 2. Transfer new .env
scp ${LOCAL_PATH}/${ENV_FILE} ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

# 3. Verify transfer
ssh ... "ls -lh ${REMOTE_PATH}/${ENV_FILE}"
```

---

### Deployment Execution Script

**File**: `.github/workflows/scripts/dev_org1_deploy.sh`

#### Purpose
Executes Docker deployment on remote servers with comprehensive health checks.

#### Operations

1. **Navigate to Application Directory**
   ```bash
   cd /datadisk/org1/react-ui
   ```

2. **Pre-Deployment Health Check**
   ```bash
   df -h /  # Check disk space
   ```

3. **Stop Existing Containers**
   ```bash
   docker compose --env-file .env.dev down
   ```

4. **Pull New Docker Image**
   ```bash
   docker compose --env-file .env.dev pull
   ```

5. **Start Updated Containers**
   ```bash
   docker compose --env-file .env.dev up -d
   ```

6. **Wait for Initialization**
   ```bash
   sleep 5  # Allow containers to start
   ```

7. **Verify Container Status**
   ```bash
   docker compose ps
   ```

8. **Health Check Verification**
   ```bash
   # Check container exists
   docker inspect org1-dev-ui

   # Check container is running
   docker inspect -f '{{.State.Running}}' org1-dev-ui
   ```

#### Error Handling

- Exits immediately on any failure
- Displays container status on errors
- Provides detailed error messages

---

## ⚙️ Configuration

### Docker Compose Configuration

Create a `docker-compose.yml` in your application repository:

```yaml
version: '3.8'

services:
  react-ui:
    image: ${REGISTRY_NAME}/react-ui-${ENVIRONMENT}:${service_version}
    container_name: org1-${ENVIRONMENT}-ui
    ports:
      - "3000:80"
    environment:
      - NODE_ENV=${NODE_ENV}
      - API_URL=${API_URL}
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Environment File Template

`.env.dev` example:

```bash
# Version Management
service_version=v1.0.0

# Environment
ENVIRONMENT=dev
NODE_ENV=development

# Docker Registry
REGISTRY_NAME=registry.example.com

# Application Configuration
API_URL=https://api-dev.example.com
APP_PORT=3000

# Feature Flags
ENABLE_DEBUG=true
```

### GitHub Actions Runner Configuration

#### Self-Hosted Runner Setup

1. **Navigate to Repository Settings** → Actions → Runners → New self-hosted runner

2. **Download and Configure Runner**:
   ```bash
   # Create runner directory
   mkdir actions-runner && cd actions-runner

   # Download latest runner
   curl -o actions-runner-linux-x64-2.311.0.tar.gz \
     -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

   # Extract
   tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

   # Configure
   ./config.sh --url https://github.com/YOUR_ORG/DevOps-CICD --token YOUR_TOKEN

   # Install as service
   sudo ./svc.sh install
   sudo ./svc.sh start
   ```

3. **Label the Runner**:
   - Use label `cicd` for build runner
   - Use label `web3` for deployment trigger runner

---

## 📖 Usage Guide

### Scenario 1: Deploy Patch Update to DEV

1. **Trigger Build Workflow**
   - Go to Actions → Multi-Environment React Frontend Build
   - Click "Run workflow"
   - Select:
     - Environment: `dev`
     - Version Type: `patch`
   - Click "Run workflow"

2. **Monitor Build Progress**
   - View real-time logs
   - Build creates image: `react-ui-dev:v1.2.7`

3. **Automatic Deployment**
   - Deployment workflow auto-triggers
   - Transfers `.env` file
   - Deploys new container

4. **Verify Deployment**
   - Check GitHub Actions summary
   - Verify application: `http://dev-server:3000`

### Scenario 2: Minor Version Release to Production

1. **Build for Production**
   ```
   Environment: prod
   Version Type: minor
   ```

2. **Review Build Summary**
   ```
   Current Version: v1.5.3
   New Version: v1.6.0
   Image: registry.example.com/react-ui-prod:v1.6.0
   ```

3. **Manual Deployment Approval** (if configured)
   - Review changes
   - Approve deployment

4. **Monitor Production Deployment**
   - Watch logs for successful health checks
   - Verify production application

### Scenario 3: Rollback Deployment

If deployment fails or issues occur:

1. **SSH to Remote Server**:
   ```bash
   ssh -i /path/to/key.pem user@remote-server
   cd /home/ubuntu/Org1/react-ui
   ```

2. **Restore Backup Environment File**:
   ```bash
   cp .env.dev.rb .env.dev
   ```

3. **Redeploy Previous Version**:
   ```bash
   docker compose --env-file .env.dev down
   docker compose --env-file .env.dev up -d
   ```

4. **Verify Rollback**:
   ```bash
   docker ps
   docker logs org1-dev-ui
   ```

---

## 🔍 Troubleshooting

### Common Issues & Solutions

#### ❌ Issue: "Environment file not found"

**Cause**: Missing or incorrect `.env` file path

**Solution**:
```bash
# Verify file exists
ls -la /datadisk/react-env/ui/org1/.env.dev

# Check permissions
chmod 644 /datadisk/react-env/ui/org1/.env.dev
```

#### ❌ Issue: "SSH connection refused"

**Cause**: SSH key permissions or firewall

**Solution**:
```bash
# Fix key permissions
chmod 600 /datadisk/sshkey/key-pair.pem

# Test SSH connection
ssh -v -i /datadisk/sshkey/key-pair.pem user@remote-server

# Check firewall
sudo ufw status
```

#### ❌ Issue: "Docker image pull failed"

**Cause**: Registry authentication or network issues

**Solution**:
```bash
# Re-authenticate to registry
docker login registry.example.com -u username

# Test image pull manually
docker pull registry.example.com/react-ui-dev:v1.2.6

# Check Docker daemon
sudo systemctl status docker
```

#### ❌ Issue: "Container health check failed"

**Cause**: Container not starting properly

**Solution**:
```bash
# Check container logs
docker logs org1-dev-ui

# Inspect container
docker inspect org1-dev-ui

# Check docker-compose config
docker compose --env-file .env.dev config

# Verify port bindings
netstat -tulpn | grep 3000
```

#### ❌ Issue: "Version rollover not working"

**Cause**: Python script or semantic_version library issue

**Solution**:
```bash
# Test version script manually
python .github/workflows/scripts/pyver.py patch dev /path/to/env

# Verify Python dependencies
pip list | grep semantic

# Reinstall if needed
pip install --upgrade semantic_version
```

### Debug Mode

Enable verbose logging in scripts:

```bash
# In bash scripts, add:
set -x  # Print commands before execution

# In Python script, add logging:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Logs Location

- **GitHub Actions Logs**: Repository → Actions → Workflow Run
- **Docker Container Logs**: `docker logs org1-dev-ui`
- **System Logs**: `/var/log/syslog` or `journalctl -u docker`

---

## 🔐 Security Best Practices

### 1. Secret Management

✅ **DO:**
- Store credentials in GitHub Secrets
- Use environment variables for sensitive data
- Rotate SSH keys regularly
- Use read-only tokens where possible

❌ **DON'T:**
- Hardcode passwords in scripts
- Commit `.env` files to repository
- Share SSH private keys
- Use root user for deployments

### 2. SSH Security

```bash
# Generate strong SSH keys
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/deploy_key

# Restrict key permissions
chmod 600 ~/.ssh/deploy_key

# Use SSH config for host-specific keys
cat >> ~/.ssh/config << EOF
Host production-server
  HostName prod.example.com
  User deploy
  IdentityFile ~/.ssh/deploy_key
  StrictHostKeyChecking yes
EOF
```

### 3. Docker Security

```yaml
# Use non-root user in Dockerfile
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Scan images for vulnerabilities
- uses: crazy-max/ghaction-container-scan@v3
  with:
    severity_threshold: CRITICAL
```

### 4. Network Security

```bash
# Firewall configuration (UFW example)
sudo ufw allow from CICD_RUNNER_IP to any port 22
sudo ufw allow 3000/tcp
sudo ufw enable

# Docker network isolation
networks:
  internal:
    internal: true  # No external access
  external:
    internal: false
```

### 5. Audit & Compliance

- Enable GitHub Actions audit logs
- Monitor deployment summaries
- Track version changes in `.env` files
- Regular security reviews
- Implement approval workflows for production

---

## 🤝 Contributing

### Development Workflow

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/DevOps-CICD.git
   cd DevOps-CICD
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Update workflows or scripts
   - Add documentation
   - Test thoroughly

4. **Test Locally**
   ```bash
   # Test Python script
   python .github/workflows/scripts/pyver.py patch dev /tmp/test

   # Test bash scripts
   bash -n .github/workflows/scripts/dev_org1_deploy.sh
   ```

5. **Commit with Conventional Commits**
   ```bash
   git commit -m "feat: add support for rollback automation"
   git commit -m "fix: resolve SSH timeout in deployment script"
   git commit -m "docs: update README with troubleshooting guide"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings to all functions

**Bash:**
- Use shellcheck for linting
- Add comments for complex logic
- Use `set -euo pipefail`

**YAML:**
- 2-space indentation
- Use comments for workflow steps
- Keep workflows modular

---

## 📊 Monitoring & Metrics

### Key Metrics to Track

1. **Deployment Success Rate**
   - Track via GitHub Actions summaries
   - Target: >95% success rate

2. **Deployment Duration**
   - Measure time from trigger to completion
   - Target: <5 minutes for DEV/STG

3. **Version Release Frequency**
   - Monitor version increments per environment
   - Track major/minor/patch ratios

4. **Container Health**
   - Post-deployment uptime
   - Error rate from container logs

### Monitoring Setup

```yaml
# Add to deployment workflow
- name: Send Metrics to Monitoring
  if: always()
  run: |
    curl -X POST https://monitoring.example.com/api/metrics \
      -H "Content-Type: application/json" \
      -d '{
        "deployment": "${{ github.event.inputs.environment }}",
        "version": "${{ steps.version.outputs.service_version }}",
        "status": "${{ job.status }}",
        "duration": "${{ steps.deployment.outputs.duration }}"
      }'
```

---

## 📚 Additional Resources

### Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Semantic Versioning Specification](https://semver.org/)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)

### Related Projects
- [GitHub Actions Self-Hosted Runners](https://github.com/actions/runner)
- [Docker Compose](https://github.com/docker/compose)
- [Container Security Scanning](https://github.com/crazy-max/ghaction-container-scan)

### Support
- 📧 **Email**: support@example.com
- 💬 **Slack**: #devops-cicd
- 🐛 **Issues**: [GitHub Issues](https://github.com/vaishakhvm/DevOps-CICD/issues)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- GitHub Actions team for the excellent CI/CD platform
- Docker community for containerization tools
- Python semantic_version library maintainers
- Contributors and reviewers

---

## 📞 Contact

**Maintainer**: Vaishakh VM  
**GitHub**: [@vaishakhvm](https://github.com/vaishakhvm)  
**Repository**: [DevOps-CICD](https://github.com/vaishakhvm/DevOps-CICD)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by the DevOps Team

</div>
