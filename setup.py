#!/usr/bin/env python3
"""
Setup script for AI Administrator
"""

import sys
import subprocess
import os


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_python_version():
    """Check if Python version is adequate"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7+ is required")
        print("   Please upgrade your Python installation")
        return False
    
    print("✓ Python version is compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    print_header("Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        return False


def verify_installation():
    """Verify the installation"""
    print_header("Verifying Installation")
    
    try:
        # Try importing the main module
        import ai_admin
        print(f"✓ AI Administrator version {ai_admin.__version__} installed")
        
        # Try importing agents
        from ai_admin.agents import SystemMonitorAgent, TaskAutomationAgent, ChatInterfaceAgent
        print("✓ All agents available")
        
        return True
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        return False


def create_config():
    """Create default configuration file"""
    print_header("Configuration")
    
    if os.path.exists("config.ini"):
        print("ℹ config.ini already exists, skipping creation")
        return True
    
    try:
        import shutil
        shutil.copy("config.ini.example", "config.ini")
        print("✓ Created config.ini from template")
        print("  You can edit this file to customize settings")
        return True
    except Exception as e:
        print(f"ℹ Could not create config.ini: {e}")
        print("  This is optional, you can create it manually later")
        return True


def run_tests():
    """Run tests to verify everything works"""
    print_header("Running Tests")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "tests.test_agents", "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓ All tests passed")
            return True
        else:
            print("⚠ Some tests failed, but installation is complete")
            print("  You can still use the system")
            return True
    except Exception as e:
        print(f"ℹ Could not run tests: {e}")
        print("  Installation is complete, tests are optional")
        return True


def show_next_steps():
    """Show what to do next"""
    print_header("Setup Complete! 🎉")
    
    print("""
Your AI Administrator is ready to use!

Next steps:

  1. Run the interactive CLI:
     python main.py

  2. See a quick demo:
     python demo.py

  3. Try the examples:
     python examples.py

  4. Read the documentation:
     - QUICKSTART.md for a quick start guide
     - README.md for full documentation

  5. Run tests:
     python -m unittest tests.test_agents

Have fun with your AI Administrator! 🤖
""")


def main():
    """Main setup function"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       AI Administrator Setup                             ║
║       Setting up your AI PC management assistant         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Install Dependencies", install_dependencies),
        ("Verify Installation", verify_installation),
        ("Create Configuration", create_config),
        ("Run Tests", run_tests),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("   Please fix the errors above and try again")
            return 1
    
    show_next_steps()
    return 0


if __name__ == "__main__":
    sys.exit(main())
