pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github_token')
        REPO_URL = 'https://github.com/pyapril15/QRCodeGenerator.git'
        BUILD_DIR = 'dist'
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
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Build EXE with PyInstaller') {
            steps {
                sh 'pyinstaller --onefile --windowed --icon=resources/icons/qrcode_icon.ico --name=QRCodeGenerator --add-data=resources/styles/style.qss:resources/styles --add-data=resources/icons/qrcode_icon.ico:resources/icons --add-data=resources/config.ini:resources --hidden-import=qrcode --hidden-import=qrcode.image.pil --hidden-import=collections.abc --exclude-module=tkinter --exclude-module=_tkinter main.py'
            }
        }

        stage('Tag Release on GitHub') {
            steps {
                script {
                    def version = sh(script: "python -c \"from src.app_logic.config import config; print(config.app_version)\"", returnStdout: true).trim()
                    sh "git tag v${version}"
                    sh "git push origin v${version}"
                }
            }
        }

        stage('Create GitHub Release & Upload EXE') {
            steps {
                script {
                    def version = sh(script: "python -c \"from src.app_logic.config import config; print(config.app_version)\"", returnStdout: true).trim()
                    def exeFile = "dist/QRCodeGenerator.exe"

                    sh """
                    curl -X POST -H "Authorization: token $GITHUB_TOKEN" \\
                        -H "Accept: application/vnd.github.v3+json" \\
                        https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/releases \\
                        -d '{
                            "tag_name": "v${version}",
                            "name": "QRCodeGenerator v${version}",
                            "body": "Automated release for version ${version}",
                            "draft": false,
                            "prerelease": false
                        }'
                    """

                    sh """
                    curl -X POST -H "Authorization: token $GITHUB_TOKEN" \\
                        -H "Content-Type: application/octet-stream" \\
                        --data-binary @${exeFile} \\
                        "https://uploads.github.com/repos/pyapril15/QRCodeGenerator/releases/latest/assets?name=QRCodeGenerator.exe"
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
