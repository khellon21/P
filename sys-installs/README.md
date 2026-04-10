# System Installs (`sys-installs`)

This directory contains automated installation scripts for various system packages and tools, ensuring they are deployed safely and consistently on Ubuntu Linux machines.

## Files

* `install_aws_cli.sh`: A bash script designed to safely install the AWS Command Line Interface (v2) and its dependencies (`curl`, `unzip`). 
  
  **Features of the script:**
  * Validates that the script is run with `root`/`sudo` privileges.
  * Validates that the `apt` package manager is available.
  * Checks if the `aws` command already exists to prevent naming conflicts.
  * Interactively prompts the user before making any system changes.
  * Performs a completely silent installation of dependencies and the software.

## Citations & References

* [AWS Command Line Interface Documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) - Used as the primary reference for the official Linux installation steps (downloading the zip, unzipping, and running the install binary).
