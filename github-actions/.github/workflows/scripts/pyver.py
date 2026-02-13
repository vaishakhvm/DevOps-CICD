#!/usr/bin/env python3
"""
================================================================================
Version Management Script for Multi-Environment Builds
================================================================================
Purpose: Automates semantic versioning across multiple deployment environments
         (dev, stg, uat, prod) with intelligent auto-rollover capabilities.

Semantic Versioning Format: MAJOR.MINOR.PATCH (e.g., v1.2.5)
- MAJOR: Breaking changes or significant releases
- MINOR: New features, backward compatible
- PATCH: Bug fixes and small improvements

Auto-Rollover Logic (Smart Versioning):
- When PATCH reaches 10 → Reset to 0, increment MINOR
- When MINOR reaches 10 → Reset to 0, increment MAJOR
- This prevents version numbers from growing indefinitely

Examples of Auto-Rollover:
  v1.0.9   -> v1.0.10  (normal patch increment)
  v1.0.10  -> v1.1.0   (patch rollover to minor)
  v1.1.10  -> v1.2.0   (patch rollover to minor)
  v1.10.10 -> v2.0.0   (both patch and minor rollover to major)

Usage:
  python pyver.py <version_type> <environment> <base_path>
  
  version_type: patch|minor|major|auto
  environment:  dev|stg|uat|prod
  base_path:    Root directory containing .env files

Environment Files Expected:
  .env.dev  - Development environment
  .env.stg  - Staging environment
  .env.uat  - User Acceptance Testing environment
  .env.prod - Production environment

Each .env file must contain: service_version=vX.Y.Z
================================================================================
"""

import os
import sys
import semantic_version


# ============================================================================
# Environment File Path Resolution
# ============================================================================
def get_env_file_path(environment, base_path):
    """
    Resolve the environment file path based on the target environment.
    
    Args:
        environment (str): Target environment (dev/stg/uat/prod)
        base_path (str): Base directory path containing .env files
    
    Returns:
        str: Full path to the environment file, or None if invalid environment
    
    Example:
        get_env_file_path('dev', '/app') -> '/app/.env.dev'
    """
    # Map environment names to their respective .env files
    env_files = {
        'dev': f'{base_path}/.env.dev',    # Development
        'stg': f'{base_path}/.env.stg',    # Staging
        'uat': f'{base_path}/.env.uat',    # User Acceptance Testing
        'prod': f'{base_path}/.env.prod'   # Production
    }
    return env_files.get(environment)


# ============================================================================
# Version Reading from Environment File
# ============================================================================
def read_current_version(env_file_path):
    """
    Extract the current version number from the environment file.
    
    Searches for 'service_version=' in the .env file and extracts the version.
    Handles versions with or without 'v' prefix (v1.2.3 or 1.2.3).
    
    Args:
        env_file_path (str): Path to the environment file
    
    Returns:
        str: Current version number (without 'v' prefix)
    
    Raises:
        FileNotFoundError: If environment file doesn't exist
        ValueError: If service_version key not found in file
    
    Example:
        File contains: service_version=v1.2.3
        Returns: "1.2.3"
    """
    # Verify environment file exists
    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f"Environment file not found: {env_file_path}")

    # Read file and search for service_version
    with open(env_file_path, 'r') as f:
        for line in f:
            if line.startswith('service_version='):
                # Extract version value after '='
                version = line.split('=')[1].strip()
                
                # Remove 'v' prefix if present (v1.2.3 -> 1.2.3)
                if version.startswith('v'):
                    version = version[1:]
                return version

    # service_version not found in file
    raise ValueError(f"service_version not found in {env_file_path}")


# ============================================================================
# Intelligent Version Increment Logic
# ============================================================================
def increment_version(current_version, version_type):
    """
    Increment version based on type with intelligent auto-rollover.
    
    Version Types:
        - 'major': Increment major version (1.2.3 -> 2.0.0)
        - 'minor': Increment minor version (1.2.3 -> 1.3.0)
        - 'patch': Increment patch with rollover (1.0.10 -> 1.1.0)
        - 'auto':  Same as patch with rollover logic
    
    Rollover Rules:
        - patch > 10  → patch=0, minor++
        - minor > 10  → minor=0, major++
    
    Args:
        current_version (str): Current version (e.g., "1.2.3")
        version_type (str): Type of increment (patch/minor/major/auto)
    
    Returns:
        str: New version string (e.g., "1.2.4")
    
    Raises:
        ValueError: If version_type is invalid
    
    Examples:
        increment_version("1.0.9", "patch")  -> "1.0.10"
        increment_version("1.0.10", "patch") -> "1.1.0"
        increment_version("1.2.3", "minor")  -> "1.3.0"
        increment_version("1.2.3", "major")  -> "2.0.0"
    """
    # Parse version string into semantic version object
    version = semantic_version.Version(current_version)
    major, minor, patch = version.major, version.minor, version.patch

    # ------------------------------------------------------------------------
    # Manual Major Version Bump
    # Resets minor and patch to 0
    # Example: 1.5.8 -> 2.0.0
    # ------------------------------------------------------------------------
    if version_type == 'major':
        return str(version.next_major())

    # ------------------------------------------------------------------------
    # Manual Minor Version Bump
    # Resets patch to 0, keeps major
    # Example: 1.5.8 -> 1.6.0
    # ------------------------------------------------------------------------
    elif version_type == 'minor':
        return str(version.next_minor())

    # ------------------------------------------------------------------------
    # Smart Patch Bump with Auto-Rollover
    # Increments patch, but rolls over when limits are reached
    # ------------------------------------------------------------------------
    elif version_type == 'patch':
        patch += 1
        
        # Rollover Rule 1: Patch exceeds limit
        # When patch > 10, reset patch and increment minor
        if patch > 10:
            patch = 0
            minor += 1
        
        # Rollover Rule 2: Minor exceeds limit
        # When minor > 10, reset minor and increment major
        if minor > 10:
            minor = 0
            major += 1
        
        return f"{major}.{minor}.{patch}"

    # ------------------------------------------------------------------------
    # Auto Mode (Explicit Auto-Rollover)
    # Same logic as patch, but can be explicitly called as 'auto'
    # Useful for CI/CD pipelines that want automatic versioning
    # ------------------------------------------------------------------------
    elif version_type == 'auto':
        patch += 1
        
        # Apply same rollover rules as patch
        if patch >= 10:
            patch = 0
            minor += 1
        if minor >= 10:
            minor = 0
            major += 1
        
        return f"{major}.{minor}.{patch}"

    # ------------------------------------------------------------------------
    # Invalid Version Type
    # ------------------------------------------------------------------------
    else:
        raise ValueError(f"Invalid version type: {version_type}")


# ============================================================================
# Environment File Update
# ============================================================================
def update_env_file(env_file_path, new_version):
    """
    Update the environment file with the new version number.
    
    Preserves all existing key-value pairs in the .env file while updating
    only the service_version value. Adds 'v' prefix to version.
    
    Args:
        env_file_path (str): Path to the environment file
        new_version (str): New version number (without 'v' prefix)
    
    Returns:
        bool: True if update successful
    
    Raises:
        FileNotFoundError: If environment file doesn't exist
    
    Process:
        1. Read all existing key-value pairs
        2. Update service_version with new value
        3. Write all pairs back to file
        4. Maintains file format: key=value
    """
    # Verify file exists
    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f"Environment file not found: {env_file_path}")

    # Read all existing environment variables
    existing_content = {}
    with open(env_file_path, 'r') as f:
        for line in f:
            # Parse non-comment lines with key=value format
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                existing_content[key.strip()] = value.strip()

    # Update service_version with 'v' prefix
    existing_content['service_version'] = f'v{new_version}'

    # Write updated content back to file
    with open(env_file_path, 'w') as f:
        for key, value in existing_content.items():
            f.write(f'{key}={value}\n')

    print(f"✅ Updated {env_file_path} with version v{new_version}")
    return True


# ============================================================================
# Input Validation
# ============================================================================
def validate_inputs(version_type, environment):
    """
    Validate command-line input parameters.
    
    Ensures version_type and environment are within acceptable values
    before processing to prevent errors downstream.
    
    Args:
        version_type (str): Type of version increment
        environment (str): Target deployment environment
    
    Raises:
        ValueError: If inputs are not in valid lists
    
    Valid Values:
        version_type: patch, minor, major, auto
        environment:  dev, stg, uat, prod
    """
    valid_version_types = ['patch', 'minor', 'major', 'auto']
    valid_environments = ['dev', 'stg', 'uat', 'prod']

    # Validate version type
    if version_type not in valid_version_types:
        raise ValueError(
            f"Invalid version type: {version_type}. "
            f"Must be one of: {valid_version_types}"
        )
    
    # Validate environment
    if environment not in valid_environments:
        raise ValueError(
            f"Invalid environment: {environment}. "
            f"Must be one of: {valid_environments}"
        )


# ============================================================================
# Main Execution Flow
# ============================================================================
def main():
    """
    Main function orchestrating the version update process.
    
    Execution Flow:
        1. Parse command-line arguments
        2. Validate inputs
        3. Locate environment file
        4. Read current version
        5. Calculate new version
        6. Update environment file
        7. Report results
    
    Command-Line Arguments:
        sys.argv[1]: version_type (patch/minor/major/auto)
        sys.argv[2]: environment (dev/stg/uat/prod)
        sys.argv[3]: base_path (directory containing .env files)
    
    Exit Codes:
        0: Success
        1: Error occurred (validation, file not found, etc.)
    
    Example Usage:
        python pyver.py patch dev /app
        python pyver.py minor stg /workspace
        python pyver.py major prod /home/user/project
    """
    # ------------------------------------------------------------------------
    # Argument Validation
    # ------------------------------------------------------------------------
    if len(sys.argv) != 4:
        print("Usage: python pyver.py <version_type> <environment> <base_path>")
        print("version_type: patch, minor, major, auto")
        print("environment: dev, stg, uat, prod")
        sys.exit(1)

    # Parse command-line arguments
    version_type = sys.argv[1]  # Type of version increment
    environment = sys.argv[2]   # Target environment
    base_path = sys.argv[3]     # Base directory path

    try:
        # ------------------------------------------------------------------------
        # Input Validation & Setup
        # ------------------------------------------------------------------------
        validate_inputs(version_type, environment)
        env_file_path = get_env_file_path(environment, base_path)
        
        if not env_file_path:
            raise ValueError(
                f"Unable to determine env file path for environment: {environment}"
            )

        # ------------------------------------------------------------------------
        # Display Processing Information
        # ------------------------------------------------------------------------
        print(f"🔄 Processing version update for {environment} environment")
        print(f"📁 Environment file: {env_file_path}")
        print(f"📈 Version type: {version_type}")

        # ------------------------------------------------------------------------
        # Read Current Version
        # ------------------------------------------------------------------------
        current_version = read_current_version(env_file_path)
        print(f"📊 Current version: v{current_version}")

        # ------------------------------------------------------------------------
        # Calculate New Version
        # ------------------------------------------------------------------------
        new_version = increment_version(current_version, version_type)
        print(f"🆕 New version: v{new_version}")

        # ------------------------------------------------------------------------
        # Update Environment File
        # ------------------------------------------------------------------------
        if update_env_file(env_file_path, new_version):
            print(f"✅ Version successfully updated from v{current_version} to v{new_version}")
        else:
            print("❌ Failed to update version")
            sys.exit(1)

    except Exception as e:
        # ------------------------------------------------------------------------
        # Error Handling
        # Catches all exceptions and provides user-friendly error messages
        # ------------------------------------------------------------------------
        print(f"❌ Error: {e}")
        sys.exit(1)


# ============================================================================
# Script Entry Point
# ============================================================================
if __name__ == "__main__":
    main()
