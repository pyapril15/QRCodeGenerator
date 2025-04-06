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
                bat '''
                    "C:\\Program Files\\Git\\bin\\git.exe" config user.name "Jenkins"
                    "C:\\Program Files\\Git\\bin\\git.exe" config user.email "jenkins@example.com"
                    "C:\\Program Files\\Git\\bin\\git.exe" tag %VERSION%
                    "C:\\Program Files\\Git\\bin\\git.exe" push origin %VERSION%
                '''
            }
        }

        stage('Create GitHub Release') {
            steps {
                bat """
                    curl -s -X POST https://api.github.com/repos/pyapril15/${REPO_NAME}/releases ^
                    -H "Authorization: token ${GITHUB_TOKEN}" ^
                    -H "Content-Type: application/json" ^
                    -d "{ \\"tag_name\\": \\"${VERSION}\\", \\"name\\": \\"${VERSION}\\", \\"body\\": \\"Automated release by Jenkins.\\", \\"draft\\": false, \\"prerelease\\": false }" > response.json

                    for /f "tokens=* usebackq" %%f in (`type response.json ^| python -c "import sys, json; print(json.load(sys.stdin)['upload_url'].split('{')[0])"`) do set UPLOAD_URL=%%f

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
