pipeline {
    agent any

    environment {
        // 🔧 Project Configuration
        PROJECT_NAME     = "QRCodeGenerator"
        VERSION          = "v1.0.3"
        REPO             = "pyapril15/${PROJECT_NAME}"
        BUILD_DIR        = "dist"
        EXE_NAME         = "${PROJECT_NAME}.exe"
        BUILD_PATH       = "${BUILD_DIR}/${EXE_NAME}"

        // 🏷️ Release Metadata
        RELEASE_NAME     = "QRCode Generator ${VERSION}"
        RELEASE_FILENAME = "release.json"

        // 📝 Markdown Release Notes File
        RELEASE_NOTES_MD = "latest_version.md"

        // 🌐 GitHub API Endpoint
        GITHUB_API_URL   = "https://api.github.com/repos/${REPO}/releases"
    }

    stages {

        stage('🔄 Checkout Code') {
            steps {
                echo "📁 Cloning repository..."
                checkout scm
            }
        }

        stage('⚙️ Setup Environment') {
            steps {
                echo "📦 Installing Python dependencies..."
                bat 'pip install -r requirements.txt'
            }
        }

        stage('🏗️ Build Executable') {
            steps {
                echo "🚧 Building Windows executable using PyInstaller..."
                bat '''
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
                echo "🔖 Tagging release version: ${VERSION}"
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
                echo "📝 Generating release.json from latest_version.md..."

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
                echo "📁 Uploading compiled .exe to GitHub release..."
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'github-token')]) {
                    bat '''
                        REM Get upload_url from response.json
                        for /F "tokens=* delims=" %%A in ('powershell -Command "(Get-Content response.json | ConvertFrom-Json).upload_url"') do (
                            set "UPLOAD_URL=%%A"
                        )

                        setlocal enabledelayedexpansion
                        set "UPLOAD_URL=!UPLOAD_URL:{?name,label}=!"

                        if not exist %BUILD_PATH% (
                            echo ❌ ERROR: %BUILD_PATH% not found!
                            exit /b 1
                        )

                        echo ⬆️ Uploading %EXE_NAME% to !UPLOAD_URL!
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
            echo "✅ Release v${VERSION} complete: Executable uploaded and published on GitHub."
        }
        failure {
            echo "❌ Build or release failed. Check the console output for detailed logs."
        }
    }
}
