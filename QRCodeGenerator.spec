# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('resources', 'resources'), ('src', 'src')]
datas += collect_data_files('PySide6')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'shiboken6', 'qrcode', 'qrcode.image.pil', 'qrcode.image.styledpil', 'qrcode.image.svg', 'collections.abc', 'PIL', 'PIL.Image', 'src.app_logic.logger', 'src.app_logic.config', 'src.app_logic.qrcode_logic', 'src.app_logic.update_logic', 'src.app_ui.ui_update_window', 'requests', 'json', 'configparser', 'pathlib', 'typing'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', '_tkinter', 'matplotlib'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='QRCodeGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\icons\\qrcode_icon.ico'],
)
