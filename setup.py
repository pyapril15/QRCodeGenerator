"""
Setup script for building the QR Code Generator executable
Author: QR Code Generator Team
Version: 1.0.0
"""

import os
import shutil
import sys

import PyInstaller.__main__


def build_executable():
    """Build the executable using PyInstaller"""

    # Application information
    APP_NAME = 'QRCodeGenerator'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Advanced QR Code Generator with PySide6'
    APP_AUTHOR = 'QR Code Generator Team'

    # Define the build arguments
    args = [
        '--onefile',  # Create a one-file bundled executable
        '--windowed',  # Hide console window (GUI app)
        '--name=' + APP_NAME,  # Name of the executable
        '--distpath=dist',  # Output directory
        '--workpath=build',  # Temporary build directory
        '--specpath=.',  # Spec file location
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without asking
        '--optimize=2',  # Optimize bytecode
        '--noupx',  # Don't use UPX compression

        # Icon (if available)
        '--icon=resources/icons/qrcode_icon.ico',

        # Hidden imports for PySide6
        '--hidden-import=PySide6',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=shiboken6',

        # Hidden imports for QR Code functionality
        '--hidden-import=qrcode',
        '--hidden-import=qrcode.image.pil',
        '--hidden-import=qrcode.image.styledpil',
        '--hidden-import=qrcode.image.svg',
        '--hidden-import=collections.abc',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',

        # Application modules
        '--hidden-import=src.app_logic.logger',
        '--hidden-import=src.app_logic.config',
        '--hidden-import=src.app_logic.qrcode_logic',
        '--hidden-import=src.app_logic.update_logic',
        '--hidden-import=src.app_ui.ui_update_window',

        # Other dependencies
        '--hidden-import=requests',
        '--hidden-import=json',
        '--hidden-import=configparser',
        '--hidden-import=pathlib',
        '--hidden-import=typing',

        # Collect data for PySide6
        '--collect-data=PySide6',

        # Add data files
        '--add-data=resources;resources',
        '--add-data=src;src',

        # Exclude unnecessary modules
        '--exclude-module=tkinter',
        '--exclude-module=_tkinter',
        '--exclude-module=matplotlib',

        # Main Python file
        'main.py'
    ]

    print("=" * 60)
    print(f"Building {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print(f"Platform: {sys.platform}")
    print(f"Python version: {sys.version}")
    print()

    try:
        # Check if icon exists
        icon_path = 'resources/icons/qrcode_icon.ico'
        if not os.path.exists(icon_path):
            print("Warning: Icon file not found. Building without icon.")
            # Remove icon argument
            args = [arg for arg in args if not arg.startswith('--icon=')]
        else:
            print(f"Using icon: {icon_path}")

        # Check for required directories
        required_dirs = ['src', 'resources']
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                print(f"Warning: Required directory '{dir_name}' not found!")

        # Run PyInstaller
        print("Starting build process...")
        PyInstaller.__main__.run(args)

        print()
        print("=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print(f"Executable location: {os.path.abspath('dist/' + APP_NAME + '.exe')}")

        # Create distribution files
        create_distribution_files(APP_NAME, APP_VERSION, APP_AUTHOR)

        print("\nDistribution files created successfully!")
        print("\nYour QR Code Generator is ready to distribute!")

    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)


def create_distribution_files(app_name, app_version, app_author):
    """Create additional distribution files"""

    # Create README for distribution
    dist_readme = f"""QR Code Generator - Distribution Package

Application: {app_name}
Version: {app_version}
Author: {app_author}
Build Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FEATURES:
✓ Advanced QR Code Generation
✓ Multiple QR Code Formats
✓ Custom Styling Options
✓ Modern PySide6 Interface
✓ Auto-Update Functionality
✓ High-Quality Output
✓ Batch Processing
✓ Export Options
✓ Professional Design
✓ Easy-to-Use Interface

CONTENTS:
- {app_name}.exe         : Main application executable
- README_DIST.txt        : This file
- LICENSE.txt            : License information

SYSTEM REQUIREMENTS:
- Windows 7/8/10/11 (64-bit recommended)
- Minimum 4GB RAM
- 100MB free disk space
- Internet connection (for updates)

INSTALLATION:
1. Simply run {app_name}.exe
2. No additional installation required
3. Application will create config files automatically

COPYRIGHT:
© 2025 {app_author}. All rights reserved.
Licensed under MIT License - see LICENSE.txt for details.
"""

    try:
        with open('dist/README_DIST.txt', 'w', encoding='utf-8') as f:
            f.write(dist_readme)
    except Exception as e:
        print(f"Warning: Could not create dist README: {e}")

    # Copy additional files to dist
    files_to_copy = [
        ('LICENSE', 'LICENSE.txt'),
        ('README.md', 'README.md'),
    ]

    for src, dst in files_to_copy:
        try:
            if os.path.exists(src):
                shutil.copy2(src, f'dist/{dst}')
        except Exception as e:
            print(f"Warning: Could not copy {src}: {e}")


def clean_build_files():
    """Clean up build files"""
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['QRCodeGenerator.spec']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"Cleaned up: {dir_name}")
            except Exception as e:
                print(f"Warning: Could not remove {dir_name}: {e}")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"Cleaned up: {file_name}")
            except Exception as e:
                print(f"Warning: Could not remove {file_name}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Build QR Code Generator executable')
    parser.add_argument('--clean', action='store_true', help='Clean build files after building')
    parser.add_argument('--test', action='store_true', help='Test the built executable')

    args = parser.parse_args()

    # Check if required files exist
    if not os.path.exists('main.py'):
        print("Error: main.py not found!")
        print("Please ensure you are running this script from the project directory.")
        sys.exit(1)

    # Check for required directories
    if not os.path.exists('src'):
        print("Error: src directory not found!")
        print("Please ensure you are running this script from the project directory.")
        sys.exit(1)

    # Check for resources directory
    if not os.path.exists('resources'):
        print("Warning: resources directory not found. Creating resources structure...")
        os.makedirs('resources/icons', exist_ok=True)
        os.makedirs('resources/styles', exist_ok=True)
        print("Please place your qrcode_icon.ico file in resources/icons/ directory")
        print("Please place your style.qss file in resources/styles/ directory")

    # Build the executable
    build_executable()

    # Test the executable if requested
    if args.test:
        print("\nTesting the executable...")
        try:
            import subprocess

            exe_path = 'dist/QRCodeGenerator.exe'
            if os.path.exists(exe_path):
                print(f"Launching {exe_path} for testing...")
                subprocess.Popen([exe_path])
                print("Executable launched successfully!")
            else:
                print("Error: Executable not found for testing.")
        except Exception as e:
            print(f"Error testing executable: {e}")

    # Clean up if requested
    if args.clean:
        print("\nCleaning up build files...")
        clean_build_files()

    print("\n" + "=" * 60)
    print("Build process completed!")
    print("=" * 60)
    print("\nFiles created in 'dist' directory:")
    print("• QRCodeGenerator.exe - Main application")
    print("• README_DIST.txt - User documentation")
    print("• LICENSE.txt - License information")
    print("\nYour QR Code Generator is ready for distribution!")
