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
                sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Get Version') {
            steps {
                script {
                    def version = sh(script: '''
                        source venv/bin/activate
                        python -c "from src.app_logic.config import config; print(config.app_version)"
                    ''', returnStdout: true).trim()
                    env.VERSION = "v${version}"
                }
            }
        }

        stage('Build EXE') {
            steps {
                sh '''
                    source venv/bin/activate
                    pyinstaller --onefile --windowed \
                    --icon=resources/icons/qrcode_icon.ico --name=QRCodeGenerator \
                    --add-data=resources/styles/style.qss:resources/styles \
                    --add-data=resources/icons/qrcode_icon.ico:resources/icons \
                    --add-data=resources/config.ini:resources \
                    --hidden-import=qrcode --hidden-import=qrcode.image.pil \
                    --hidden-import=collections.abc --exclude-module=tkinter --exclude-module=_tkinter main.py
                '''
            }
        }

        stage('Tag & Push') {
            steps {
                sh '''
                    git config user.name "pyapril15"
                    git config user.email "praveen885127@gmail.com"
                    git tag ${VERSION}
                    git push origin ${VERSION}
                '''
            }
        }

        stage('Create GitHub Release') {
            steps {
                sh '''
                    curl -s -X POST https://api.github.com/repos/pyapril15/${REPO_NAME}/releases \
                    -H "Authorization: token ${GITHUB_TOKEN}" \
                    -H "Content-Type: application/json" \
                    -d '{
                        "tag_name": "'${VERSION}'",
                        "name": "'${VERSION}'",
                        "body": "Automated release by Jenkins.",
                        "draft": false,
                        "prerelease": false
                    }' > response.json

                    UPLOAD_URL=$(cat response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['upload_url'].split('{')[0])")
                    curl -s -X POST "$UPLOAD_URL?name=QRCodeGenerator.exe" \
                    -H "Authorization: token ${GITHUB_TOKEN}" \
                    -H "Content-Type: application/octet-stream" \
                    --data-binary @"${DIST_DIR}/QRCodeGenerator/QRCODEGENERATOR.exe"
                '''
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
