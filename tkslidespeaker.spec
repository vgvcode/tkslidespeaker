# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tkslidespeaker.py'],
    binaries=[],
    datas=[
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\default.pptx', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\notesMaster.xml', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\theme.xml', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\notes.xml', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\docx-icon.emf', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\generic-icon.emf', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\pptx-icon.emf', '.\\pptx\\templates\\'),
        ('..\\..\\..\\..\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\pptx\\templates\\xlsx-icon.emf', '.\\pptx\\templates\\')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='tkslidespeaker',
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
