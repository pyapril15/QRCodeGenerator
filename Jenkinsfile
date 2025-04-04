pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github_token')
        REPO_URL = 'https://github.com/pyapril15/QRCodeGenerator.git'
        BUILD_DIR = 'dist'
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: env.REPO_URL
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    def pythonInstalled = sh(script: "python3 --version || python --version", returnStatus: true) == 0
                    if (!pythonInstalled) {
                        error("Python is not installed on the system")
                    }
                }
                sh 'python3 -m venv $VENV_DIR'
                sh '. $VENV_DIR/bin/activate'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Build EXE with PyInstaller') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate && pyinstaller --onefile --windowed \
                    --icon=resources/icons/qrcode_icon.ico --name=QRCodeGenerator \
                    --add-data=resources/styles/style.qss:resources/styles \
                    --add-data=resources/icons/qrcode_icon.ico:resources/icons \
                    --add-data=resources/config.ini:resources \
                    --hidden-import=qrcode --hidden-import=qrcode.image.pil \
                    --hidden-import=collections.abc --exclude-module=tkinter --exclude-module=_tkinter main.py
                '''
            }
        }

        stage('Determine Version & Tag Release') {
            steps {
                script {
                    def version = sh(script: ". $VENV_DIR/bin/activate && python -c \"from src.app_logic.config import config; print(config.app_version)\"", returnStdout: true).trim()

                    if (!version || version == "None") {
                        error("Failed to retrieve version from config")
                    }

                    sh """
                    git config user.name "Jenkins"
                    git config user.email "jenkins@example.com"
                    git tag -a v${version} -m "Release v${version}"
                    git push origin v${version}
                    """
                }
            }
        }

        stage('Create GitHub Release & Upload EXE') {
            steps {
                script {
                    def version = sh(script: ". $VENV_DIR/bin/activate && python -c \"from src.app_logic.config import config; print(config.app_version)\"", returnStdout: true).trim()
                    def exeFile = "dist/QRCodeGenerator.exe"

                    if (!fileExists(exeFile)) {
                        error("Executable file not found: ${exeFile}")
                    }

                    def releaseResponse = sh(script: """
                    curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
                        -H "Accept: application/vnd.github.v3+json" \
                        https://api.github.com/repos/pyapril15/QRCodeGenerator/releases \
                        -d '{
                            "tag_name": "v${version}",
                            "name": "QRCodeGenerator v${version}",
                            "body": "Automated release for version ${version}",
                            "draft": false,
                            "prerelease": false
                        }'
                    """, returnStdout: true).trim()

                    echo "GitHub Release Response: ${releaseResponse}"

                    def uploadUrl = sh(script: """
                    echo '${releaseResponse}' | jq -r .upload_url | sed 's/{?name,label}//'
                    """, returnStdout: true).trim()

                    if (!uploadUrl || uploadUrl == "null") {
                        error("Failed to retrieve upload URL from GitHub response")
                    }

                    sh """
                    curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
                        -H "Content-Type: application/octet-stream" \
                        --data-binary @${exeFile} \
                        "${uploadUrl}?name=QRCodeGenerator.exe"
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build and Release Completed Successfully!"
        }
        failure {
            echo "❌ Build or Release Failed! Check logs."
        }
    }
}
