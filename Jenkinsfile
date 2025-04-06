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
                    ''', returnStdout: true).trim().split("\r?\n")[-1] // get last line
                    env.VERSION = "v${version}"
                }
            }
        }

        stage('Build EXE') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pyinstaller --onefile --windowed \
                    --icon=resources\\icons\\qrcode_icon.ico --name=QRCodeGenerator \
                    --add-data=resources\\styles\\style.qss;resources/styles \
                    --add-data=resources\\icons\\qrcode_icon.ico;resources/icons \
                    --add-data=resources\\config.ini;resources \
                    --hidden-import=qrcode --hidden-import=qrcode.image.pil \
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

                    git fetch --tags
                    git tag -d ${env.VERSION} 2>NUL
                    git tag ${env.VERSION}
                    git push origin ${env.VERSION}
                """
            }
        }


        stage('Create GitHub Release') {
            steps {
                sh """
                    curl -s -X POST https://api.github.com/repos/pyapril15/${REPO_NAME}/releases ^
                    -H "Authorization: token ${GITHUB_TOKEN}" ^
                    -H "Accept: application/vnd.github.v3+json" ^
                    -d "{ \\"tag_name\\": \\"${VERSION}\\", \\"name\\": \\"${VERSION}\\", \\"body\\": \\"Automated release by Jenkins.\\", \\"draft\\": false, \\"prerelease\\": false }" ^
                    -o response.json

                    for /f "usebackq tokens=*" %%i in (`jq -r ".upload_url" response.json`) do set URL=%%i
                    for /f "tokens=1 delims={ " %%u in ("!URL!") do set UPLOAD_URL=%%u

                    curl -s -X POST "!UPLOAD_URL!?name=QRCodeGenerator.exe" ^
                    -H "Authorization: token ${GITHUB_TOKEN}" ^
                    -H "Content-Type: application/octet-stream" ^
                    --data-binary @"${DIST_DIR}\\QRCodeGenerator.exe"
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
