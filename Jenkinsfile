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
					bat '''
						echo Creating GitHub release...

						REM Step 1: Create the GitHub release and save response
						curl -s -X POST https://api.github.com/repos/pyapril15/QRCodeGenerator/releases ^
							-H "Authorization: token %TOKEN%" ^
							-H "Accept: application/vnd.github.v3+json" ^
							-d "{ \\"tag_name\\": \\"${VERSION}\\", \\"name\\": \\"QRCode Generator ${VERSION}\\", \\"body\\": \\"🚀 New release of QRCodeGenerator!\\\\n\\\\n🔹 Version: ${VERSION}\\\\n🔹 Platform: Windows (.exe)\\\\n\\\\nThis release includes all the latest features, fixes, and enhancements.\\\\n\\\\n✨ Enjoy generating beautiful QR codes with ease.\\", \\"draft\\": false, \\"prerelease\\": false }" ^
							-o response.json

						REM Step 2: Extract upload_url using PowerShell
						for /f "tokens=* delims=" %%A in ('powershell -Command "(Get-Content response.json | ConvertFrom-Json).upload_url"') do (
							set "UPLOAD_URL=%%A"
						)

						REM Step 3: Sanitize URL
						setlocal enabledelayedexpansion
						set "UPLOAD_URL=!UPLOAD_URL:{?name,label}=!"

						REM Step 4: Check if EXE exists
						if not exist dist\\QRCodeGenerator.exe (
							echo ❌ ERROR: dist\\QRCodeGenerator.exe not found!
							exit /b 1
						)

						REM Step 5: Upload EXE to GitHub release
						echo Uploading EXE to !UPLOAD_URL!
						curl -s -X POST "!UPLOAD_URL!?name=QRCodeGenerator.exe" ^
							-H "Authorization: token %TOKEN%" ^
							-H "Content-Type: application/octet-stream" ^
							--data-binary "@dist\\QRCodeGenerator.exe"
						if errorlevel 1 (
							echo ❌ ERROR: Upload failed!
							exit /b 2
						) else (
							echo ✅ EXE uploaded successfully.
						)
					'''
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
