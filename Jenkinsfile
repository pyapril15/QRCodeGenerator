pipeline {
	agent any

    environment {
		REPO = 'https://github.com/pyapril15/QRCodeGenerator.git'
        REPO_NAME = 'QRCodeGenerator'
        DIST_DIR = 'dist'
        EXE_NAME = 'QRCodeGenerator.exe'
    }

    stages {
		stage('Clone Repo') {
			steps {
				git url: "${env.REPO}", branch: 'main'
            }
        }

        stage('Setup Python') {
			steps {
				bat '''
                    C:\\Users\\pytwl\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m venv venv
                    call venv\\Scripts\\activate
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Get Version') {
			steps {
				script {
					def version = bat(script: '''
                        call venv\\Scripts\\activate
                        python -c "from src.app_logic.config import config; print(config.app_version)"
                    ''', returnStdout: true).trim().split("\\r?\\n")[-1]
                    env.VERSION = "v${version}"
                }
            }
        }

        stage('Build EXE') {
			steps {
				bat '''
                    call venv\\Scripts\\activate
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

        stage('Tag & Push') {
			steps {
				withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
					bat """
                        echo Tagging version: ${env.VERSION}
                        git config user.name "pyapril15"
                        git config user.email "praveen885127@gmail.com"
                        git remote set-url origin https://${TOKEN}@github.com/pyapril15/QRCodeGenerator.git
                        git fetch --tags
                        git branch --set-upstream-to=origin/main main
                        git tag -d ${env.VERSION} 2>NUL
                        git tag ${env.VERSION}
                        git push origin ${env.VERSION}
                    """
                }
            }
        }

        stage('Create GitHub Release with EXE Upload') {
			steps {
				withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
					bat """
                        echo Creating GitHub release...

                        curl -s -X POST https://api.github.com/repos/pyapril15/${REPO_NAME}/releases ^
                        -H "Authorization: token %TOKEN%" ^
                        -H "Accept: application/vnd.github.v3+json" ^
                        -d "{ \\"tag_name\\": \\"${env.VERSION}\\", \\"name\\": \\"QRCode Generator ${env.VERSION}\\", \\"body\\": \\"🚀 New release of QRCodeGenerator!\\\\n\\\\n🔹 Version: ${env.VERSION}\\\\n🔹 Platform: Windows (.exe)\\\\n\\\\nThis release includes all the latest features, fixes, and enhancements.\\\\n\\\\n\\u2728 Enjoy generating beautiful QR codes with ease.\\", \\"draft\\": false, \\"prerelease\\": false }" ^
                        -o response.json

                        for /f "tokens=2 delims=:," %%A in ('findstr /i "upload_url" response.json') do (
                            set "UPLOAD_URL=%%~A"
                        )

                        setlocal enabledelayedexpansion
                        set "UPLOAD_URL=!UPLOAD_URL:~1,-1!"
                        set "UPLOAD_URL=!UPLOAD_URL:{?name,label}=!"

                        curl -s -X POST "!UPLOAD_URL!?name=${EXE_NAME}" ^
                        -H "Authorization: token %TOKEN%" ^
                        -H "Content-Type: application/octet-stream" ^
                        --data-binary "@${DIST_DIR}\\${EXE_NAME}"
                    """
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
