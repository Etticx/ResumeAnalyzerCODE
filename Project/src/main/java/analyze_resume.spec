# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\ResumeAnalyse\\ResumeAnalyzer\\Project\\src\\main\\java\\analyze_resume.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\ResumeAnalyse\\ResumeAnalyzer\\Project\\venv\\Lib\\site-packages\\en_core_web_sm\\en_core_web_sm-3.8.0', 'en_core_web_sm')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='analyze_resume',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
