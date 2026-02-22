# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for VS Animator
# Build: cd I:\CLAUDE\VSAnimator\src && py -3.11 -m PyInstaller VSAnimator.spec

block_cipher = None
src_dir = r'I:\CLAUDE\VSAnimator\src'

a = Analysis(
    [src_dir + r'\vs_animator_app.py'],
    pathex=[src_dir],
    binaries=[],
    datas=[
        (src_dir + r'\vs-animator.html', '.'),
        (src_dir + r'\presets.js', '.'),
    ],
    hiddenimports=[
        'webview',
        'clr_loader',
        'pythonnet',
        'bottle',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'unittest', 'test',
        'pydoc', 'doctest', 'difflib',
        'numpy', 'PIL', 'scipy', 'pandas',
        'setuptools', 'pkg_resources',
        'multiprocessing', 'concurrent',
        'asyncio', 'sqlite3', 'csv',
        'ftplib', 'imaplib', 'smtplib', 'poplib',
        'xmlrpc',
        'curses', 'lib2to3',
    ],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='VSAnimator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=['vcruntime140.dll', 'python3.dll'],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'I:\CLAUDE\VSAnimator\dist\VSAnimator.ico',
)
