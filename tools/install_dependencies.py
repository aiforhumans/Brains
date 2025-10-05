#!/usr/bin/env python3
"""
Dependency installer for ComfyUI-DEV
Handles installation of required dependencies with graceful fallbacks
"""

import subprocess
import sys
import os

def check_and_install_torch():
    """Check if torch is available and install if needed"""
    try:
        import torch
        print(f"âœ… Torch {torch.__version__} is already installed")
        return True
    except ImportError:
        print("âš ï¸  Torch not found. Attempting to install...")
        try:
            # Try to install torch
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "torch", "torchvision", "--index-url", "https://download.pytorch.org/whl/cpu"
            ])
            print("âœ… Torch installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"âŒ Failed to install torch: {e}")
            print("â„¹ï¸  BRAIN datatype system will still work without torch")
            return False

def install_requirements():
    """Install requirements from requirements.txt"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", requirements_path
            ])
            print("âœ… Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"âš ï¸  Some requirements failed to install: {e}")
            return False
    else:
        print("âš ï¸  requirements.txt not found")
        return False

def main():
    """Main installation process"""
    print("ðŸ”§ ComfyUI-DEV Dependency Installer")
    print("=" * 40)
    
    # Try installing from requirements.txt first
    req_success = install_requirements()
    
    # Check torch specifically (most critical dependency)
    torch_success = check_and_install_torch()
    
    print("\n" + "=" * 40)
    if torch_success:
        print("ðŸŽ‰ All critical dependencies installed!")
        print("â„¹ï¸  Both legacy and BRAIN systems should work")
    else:
        print("âš ï¸  Torch installation failed")
        print("â„¹ï¸  BRAIN datatype system will still work")
        print("â„¹ï¸  Legacy nodes require torch to function")
    
    return torch_success

if __name__ == "__main__":
    main()
