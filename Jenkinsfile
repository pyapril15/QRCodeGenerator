pipeline {
    agent any

    environment {
        PROJECT_NAME = "QRCodeGenerator"
        VERSION = "v1.0.3"
        REPO = "pyapril15/${PROJECT_NAME}"
        BUILD_PATH = "dist/${PROJECT_NAME}.exe"
        RELEASE_NAME = "QRCode Generator ${VERSION}"
        RELEASE_BODY = "🚀 New release of ${PROJECT_NAME}!\n\n🔹 Version: ${VERSION}\n🔹 Platform: Windows (.exe)\n\nThis release includes all the latest features, fixes, and enhancements.\n\n✨ Enjoy generating beautiful QR codes with ease."
    }

    stages {

        stage('🔄 Checkout') {
            steps {
                echo "Checking out code..."
                checkout scm
            }
        }

        stage('⚙️ Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                bat 'pip install -r requirements.txt'
            }
        }

        stage('📦 Build Executable') {
            steps {
                echo "Building executable using PyInstaller..."
                bat '''
                pyinstaller --onefile --windowed ^
                    --icon=resources\\icons\\qrcode_icon.ico --name=QRCodeGenerator ^
                    --add-data=resources\\styles\\style.qss;resources/styles ^
                    --add-data=resources\\icons\\qrcode_icon.ico;resources/icons ^
                    --add-data=resources\\config.ini;resources ^
                    --hidden-import=qrcode --hidden-import=qrcode.image.pil ^
                    --hidden-import=collections.abc --exclude-module=tkinter --exclude-module=_tkinter main.py
                '''
            }
        }

        stage('🏷️ Git Tag & Push') {
            steps {
                echo "Tagging release as ${VERSION} and pushing to GitHub..."
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github-token')]) {
                    bat """
                        git config user.name "pyapril15"
                        git config user.email "praveen885127@gmail.com"
                        git remote set-url origin https://%github-token%@github.com/${REPO}.git
                        git fetch --tags
                        git tag -d ${VERSION} 2>NUL
                        git tag ${VERSION}
                        git push origin ${VERSION}
                    """
                }
            }
        }

        stage('📤 Create GitHub Release') {
            steps {
                echo "Creating GitHub release..."
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github-token')]) {
                    writeFile file: 'release.json', text: """{
          "tag_name": "${VERSION}",
          "name": "${RELEASE_NAME}",
          "body": "🚀 New release of ${PROJECT_NAME}!\n\n🔹 Version: ${VERSION}\\n🔹 Platform: Windows (.exe)\\n\\nThis release includes all the latest features, fixes, and enhancements.\\n\\n✨ Enjoy generating beautiful QR codes with ease.",
          "draft": false,
          "prerelease": false
        }"""
                    bat """
                        curl -s -X POST https://api.github.com/repos/${REPO}/releases ^
                             -H "Authorization: token %github-token%" ^
                             -H "Accept: application/vnd.github.v3+json" ^
                             -d @release.json ^
                             -o response.json
                    """
                }
            }
        }


        stage('📥 Upload .exe to Release') {
            steps {
                echo "Uploading EXE to GitHub release..."
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github-token')]) {
                    bat '''
                        for /F "tokens=* delims=" %%A in ('powershell -Command "(Get-Content response.json | ConvertFrom-Json).upload_url"') do (
                            set "UPLOAD_URL=%%A"
                        )
                        setlocal enabledelayedexpansion
                        set "UPLOAD_URL=!UPLOAD_URL:{?name,label}=!"

                        if not exist %BUILD_PATH% (
                            echo ❌ ERROR: %BUILD_PATH% not found!
                            exit /b 1
                        )

                        echo Uploading EXE to !UPLOAD_URL!
                        curl -s -X POST "!UPLOAD_URL!?name=QRCodeGenerator.exe" ^
                             -H "Authorization: token %github-token%" ^
                             -H "Content-Type: application/octet-stream" ^
                             --data-binary "@%BUILD_PATH%"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build and GitHub release with .exe uploaded successfully."
        }
        failure {
            echo "❌ Build failed. Check logs for details."
        }
    }
}
