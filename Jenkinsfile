pipeline {
    agent any

    environment {
        GITHUB_REPO = 'https://github.com/pyapril15/QRCodeGenerator.git'
        GITHUB_TOKEN = credentials('github-token')  // Make sure you have set up this credential in Jenkins
        BUILD_DIR = 'build'
        DIST_DIR = 'dist'
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: "${GITHUB_REPO}", branch: 'main'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv ${VENV_DIR}'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Build EXE with PyInstaller') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                pyinstaller --onefile --windowed --icon=resources/icons/qrcode_icon.ico --name=QRCodeGenerator \
                    --add-data=resources/styles/style.qss:resources/styles \
                    --add-data=resources/icons/qrcode_icon.ico:resources/icons \
                    --add-data=resources/config.ini:resources \
                    --hidden-import=qrcode --hidden-import=qrcode.image.pil --hidden-import=collections.abc \
                    --exclude-module=tkinter --exclude-module=_tkinter main.py
                '''
            }
        }

        stage('Upload Release to GitHub') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                VERSION=$(date +%Y%m%d%H%M%S)  # Generates a timestamped version
                EXE_PATH="${DIST_DIR}/QRCodeGenerator.exe"

                # Create a new release on GitHub
                curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" -H "Accept: application/vnd.github.v3+json" \
                    https://api.github.com/repos/pyapril15/QRCodeGenerator/releases \
                    -d '{
                        "tag_name": "'${VERSION}'",
                        "name": "QRCodeGenerator Release '${VERSION}'",
                        "body": "Automated release via Jenkins",
                        "draft": false,
                        "prerelease": false
                    }' | tee release.json

                UPLOAD_URL=$(jq -r .upload_url release.json | sed "s/{?name,label}//")

                # Upload the built EXE file
                curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: application/octet-stream" \
                    --data-binary @"${EXE_PATH}" "${UPLOAD_URL}?name=QRCodeGenerator-${VERSION}.exe"
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -rf ${BUILD_DIR} ${DIST_DIR} ${VENV_DIR}'
        }
    }
}
