# QRCodeGenerator

## Overview

The QR Code Generator is a desktop application built with PySide6 that allows users to generate and customize QR codes based on their input. Users can configure various aspects of the QR code, including its version, box size, border size, fill color, and background color. The generated QR code can be saved as an image file.

## Features

- **Customizable QR Codes**: Users can customize the QR code's version, box size, border size, fill color, and background color.
- **Real-time Updates**: The QR code preview updates in real-time as the user changes the settings.
- **Save QR Code**: Generated QR codes can be saved as PNG images.
- **User-friendly Interface**: Clean and modern UI built with PySide6 and styled using QSS.

## Project Structure
QRCodeGenerator/
├── resources/
│ ├── config.ini # Configuration file
│ ├── qrcode_icon.ico # Icon file for the application
│ ├── style.qss # QSS stylesheet
├── src/
│ ├── init.py # Initialize the src package
│ ├── config.py # Configuration handling module
│ ├── logger.py # Logging module
│ ├── ui_qrcode.py # UI module generated from .ui file
├── app.log # Log file
├── main.py # Main application script
├── README.md # Project documentation
├── requirements.txt # Python dependencies


## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/pyapril15/QRCodeGenerator.git
   ```
   ```bash
   cd QRCodeGenerator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   ```
   ```bash
   venv\Scripts\activate
   ```
   
3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python src/main.py
   ```
   
## Usage

1. **Enter the text**: Type the text you want to encode into the QR code in the provided text field.

2. **Customize settings**: Adjust the version, box size, border size, fill color, and background color using the sliders and color pickers.

3. **Generate QR Code**: Click the "Generate QR Code" button to see the preview of your QR code.

4. **Save QR Code**: Click the "Save QR Code" button to save the generated QR code as a PNG image in the saved_qrcodes directory.


## Configuration
The application uses a configuration file (config.ini) located in the resources directory.
This file contains default settings for the QR code generation and paths to resources:

1. **[Settings]**:
   - DEFAULT_VERSION = 1
   - DEFAULT_BOX_SIZE = 10
   - DEFAULT_BORDER_SIZE = 4
   - DEFAULT_FILL_COLOR = black
   - DEFAULT_BACK_COLOR = white

2. **[Paths]**:
   - QSS_PATH = resources/style.qss
   - ICON_PATH = resources/qrcode_icon.ico

## Logging
The application logs events and errors to app.log. This includes successful operations and any errors that occur during execution. The log file can be used to analyze the application's behavior and diagnose issues.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or create a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or feedback, please contact praveen885127@gmail.com.
