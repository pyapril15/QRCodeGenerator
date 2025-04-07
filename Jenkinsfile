pipeline {
	agent any

    environment {
		GITHUB_TOKEN = credentials('GITHUB_TOKEN')
        REPO = 'https://github.com/pyapril15/QRCodeGenerator.git'
        REPO_NAME = 'QRCodeGenerator'
        DIST_DIR = "dist"
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
                    ''', returnStdout: true).trim().split("\r?\n")[-1]
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
				bat """
                    echo Tagging version: ${env.VERSION}
                    git config user.name "pyapril15"
                    git config user.email "praveen885127@gmail.com"

                    git remote set-url origin https://${GITHUB_TOKEN}@github.com/pyapril15/QRCodeGenerator.git
                    git fetch --tags
                    git branch --set-upstream-to=origin/main main

                    git tag -d ${env.VERSION} 2>NUL
                    git tag ${env.VERSION}
                    git push origin ${env.VERSION}

                    if %ERRORLEVEL% NEQ 0 (
                        echo ❌ Failed to push tag. Check permissions or token!
                        exit /b %ERRORLEVEL%
                    ) else (
                        echo ✅ Tag pushed successfully: ${env.VERSION}
                    )
                """
            }
        }

        stage('Create GitHub Release') {
			steps {
				bat """
                    curl -s -X POST https://api.github.com/repos/pyapril15/%REPO_NAME%/releases ^
                    -H "Authorization: token ${GITHUB_TOKEN}" ^
                    -H "Accept: application/vnd.github.v3+json" ^
                    -d "{ \\"tag_name\\": \\"${env.VERSION}\\", \\"name\\": \\"${env.VERSION}\\", \\"body\\": \\"Automated release by Jenkins.\\", \\"draft\\": false, \\"prerelease\\": false }" ^
                    -o response.json

                    type response.json
                """
            }
        }
    }

    post {
		failure {
			echo "❌ Build failed!"
        }
        success {
			echo "✅ Build and release completed successfully."
        }
    }
}
