# QRCodeGenerator

## Overview

QRCodeGenerator is a desktop application built with PySide6 that allows users to generate and customize QR codes. Users can configure various aspects of the QR code, including its version, box size, border size, fill color, and background color. The generated QR code can be saved as a PNG image.

## Features

- **Customizable QR Codes**: Adjust version, box size, border size, fill color, and background color.
- **Real-time Updates**: QR code preview updates instantly based on user settings.
- **Save QR Code**: Generated QR codes can be saved as PNG images.
- **User-friendly Interface**: Clean and modern UI styled with QSS.

## Project Structure

```
QRCodeGenerator/
├── prj_img/
│   └── qr_code_generator.png
├── resources/
│   ├── config.ini        # Configuration file
│   ├── qrcode_icon.ico   # Application icon
│   └── style.qss         # QSS stylesheet
├── src/
│   ├── __init__.py       # Initialize src package
│   ├── config.py         # Configuration handling module
│   ├── logger.py         # Logging module
│   └── ui_qrcode.py      # UI module generated from .ui file
├── app.log               # Log file
├── main.py               # Main application script
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── LICENSE               # License file
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/pyapril15/QRCodeGenerator.git
   cd QRCodeGenerator
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python main.py
   ```

## Usage

1. **Enter text**: Type the text you want to encode.
2. **Customize settings**: Adjust QR code settings using sliders and color pickers.
3. **Generate QR Code**: Click "Generate QR Code" to preview.
4. **Save QR Code**: Click "Save QR Code" to store the image in `saved_qrcodes`.

## Configuration

The `config.ini` file stores default settings:

### `[Settings]`
- `DEFAULT_VERSION = 1`
- `DEFAULT_BOX_SIZE = 10`
- `DEFAULT_BORDER_SIZE = 4`
- `DEFAULT_FILL_COLOR = black`
- `DEFAULT_BACK_COLOR = white`

### `[Paths]`
- `QSS_PATH = resources/style.qss`
- `ICON_PATH = resources/qrcode_icon.ico`

## Logging

The application logs events and errors to `app.log`, aiding in debugging and maintenance.

## Dependency Notes

Some dependencies included during packaging (e.g., `posix`, `pwd`, `grp`) are related to Unix-like systems. They do not affect core functionality on Windows.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contact

**Author:** codelabpraveen  
**Email:** praveen885127@gmail.com
