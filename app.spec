# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["app.py", "controllers/freq_drawer.py", "controllers/freq_maker.py", "controllers/freq_player.py", "views/fields.py", "views/styles.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
# a = Analysis(
#     ["app.py", "controllers/freq_drawer.py", "controllers/freq_maker.py", "controllers/freq_player.py", "views/fields.py", "views/styles.py"],
#     pathex=["."],
#     binaries=[],
#     datas=datas,
#     hiddenimports=[],
#     hookspath=[],
#     hooksconfig={},
#     runtime_hooks=[],
#     excludes=[],
#     win_no_prefer_redirects=False,
#     win_private_assemblies=False,
#     cipher=block_cipher,
#     noarchive=False,
# )
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
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
