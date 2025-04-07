pipeline {
    agent any

    environment {
        // 🔧 Project Metadata
        PROJECT_NAME     = "QRCodeGenerator"
        VERSION          = "v1.0.3"
        REPO             = "pyapril15/${PROJECT_NAME}"

        // 🛠️ Build Output
        BUILD_DIR        = "dist"
        EXE_NAME         = "${PROJECT_NAME}.exe"
        BUILD_PATH       = "${BUILD_DIR}/${EXE_NAME}"

        // 📝 Release Info
        RELEASE_NAME     = "QRCode Generator ${VERSION}"
        RELEASE_FILENAME = "release.json"
        RELEASE_NOTES_MD = "latest_version.md"

        // 🌍 GitHub
        GITHUB_API_URL   = "https://api.github.com/repos/${REPO}/releases"

        // 🐍 Python Virtual Environment Directory
        VENV_DIR         = ".venv"
    }

    stages {

        stage('🔄 Checkout Code') {
            steps {
                echo "📁 Checking out the latest source code..."
                checkout scm
            }
        }

        stage('🐍 Setup Python Virtual Environment') {
            steps {
                echo "🔧 Setting up Python virtual environment..."
                bat '''
                    REM Create virtual environment
                    python -m venv %VENV_DIR%

                    REM Activate and upgrade pip
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                '''
            }
        }

        stage('📦 Install Dependencies') {
            steps {
                echo "📚 Installing required Python packages into virtual environment..."
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pip install -r requirements.txt
                '''
            }
        }

        stage('🏗️ Build Executable with PyInstaller') {
            steps {
                echo "🛠️ Building .exe using PyInstaller inside virtual environment..."
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pyinstaller --onefile --windowed ^
                        --icon=resources\\icons\\qrcode_icon.ico --name=%PROJECT_NAME% ^
                        --add-data=resources\\styles\\style.qss;resources/styles ^
                        --add-data=resources\\icons\\qrcode_icon.ico;resources/icons ^
                        --add-data=resources\\config.ini;resources ^
                        --hidden-import=qrcode --hidden-import=qrcode.image.pil ^
                        --hidden-import=collections.abc ^
                        --exclude-module=tkinter --exclude-module=_tkinter main.py
                '''
            }
        }

        stage('🏷️ Tag & Push Git Release') {
            steps {
                echo "🔖 Tagging and pushing version: ${VERSION}"
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github-token')]) {
                    bat '''
                        git config user.name "pyapril15"
                        git config user.email "praveen885127@gmail.com"
                        git remote set-url origin https://%github-token%@github.com/%REPO%.git

                        git fetch --tags
                        git tag -d %VERSION% 2>NUL
                        git tag %VERSION%
                        git push origin %VERSION%
                    '''
                }
            }
        }

        stage('📤 Create GitHub Release') {
            steps {
                echo "📦 Preparing GitHub release JSON from markdown..."

                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github-token')]) {
                    bat '''
                        setlocal EnableDelayedExpansion

                        set "BODY="
                        for /F "usebackq delims=" %%A in ("%RELEASE_NOTES_MD%") do (
                            set "LINE=%%A"
                            set "LINE=!LINE:\"=\\\"!"
                            set "BODY=!BODY!!LINE!\\n"
                        )

                        (
                            echo {
                            echo   "tag_name": "%VERSION%",
                            echo   "name": "%RELEASE_NAME%",
                            echo   "body": "!BODY!",
                            echo   "draft": false,
                            echo   "prerelease": false
                            echo }
                        ) > %RELEASE_FILENAME%

                        curl -s -X POST %GITHUB_API_URL% ^
                             -H "Authorization: token %github-token%" ^
                             -H "Accept: application/vnd.github.v3+json" ^
                             -d @%RELEASE_FILENAME% ^
                             -o response.json
                    '''
                }
            }
        }

        stage('📥 Upload Executable to GitHub Release') {
            steps {
                echo "⬆️ Uploading .exe to GitHub release..."
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github-token')]) {
                    bat '''
                        REM Extract upload URL from API response
                        for /F "tokens=* delims=" %%A in ('powershell -Command "(Get-Content response.json | ConvertFrom-Json).upload_url"') do (
                            set "UPLOAD_URL=%%A"
                        )

                        setlocal enabledelayedexpansion
                        set "UPLOAD_URL=!UPLOAD_URL:{?name,label}=!"

                        if not exist %BUILD_PATH% (
                            echo ❌ ERROR: Executable not found at %BUILD_PATH%
                            exit /b 1
                        )

                        echo 🚀 Uploading executable to !UPLOAD_URL!
                        curl -s -X POST "!UPLOAD_URL!?name=%EXE_NAME%" ^
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
            echo "✅ SUCCESS: ${VERSION} release published with executable."
        }
        failure {
            echo "❌ FAILURE: Build or deployment process failed. Check logs for details."
        }
    }
}
