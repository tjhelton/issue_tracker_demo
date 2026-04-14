# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for SafetyCulture Tools.

Bundles the Streamlit app, pywebview, and all dependencies into a
standalone executable.  Produces a .app bundle on macOS and a folder
with an .exe on Windows.

Build:  pyinstaller "SafetyCulture Tools.spec"
Output: dist/SafetyCulture Tools.app  (Mac)
        dist/SafetyCulture Tools/     (Windows)
"""

import sys
from PyInstaller.utils.hooks import collect_all

# ── Pre-collect package data BEFORE Analysis ───────────────────────────
# collect_all() returns (datas, binaries, hiddenimports) as *input* format
# (2-tuple datas/binaries).  They must be fed into Analysis(), not appended
# to a.datas after the fact — appending post-Analysis mixes 2-tuple input
# format with the 3-tuple internal TOC format and breaks PyInstaller 6.x.

extra_datas = []
extra_binaries = []
extra_hiddenimports = [
    # Streamlit internals
    "streamlit.web.cli",
    "streamlit.web.bootstrap",
    "streamlit.runtime.scriptrunner",
    "streamlit.runtime.scriptrunner.magic_funcs",
    "streamlit.runtime.state",
    "streamlit.components.v1",
    # Tornado (Streamlit's web server)
    "tornado",
    "tornado.web",
    "tornado.httpserver",
    "tornado.ioloop",
    "tornado.websocket",
    # Click (Streamlit CLI)
    "click",
    # Typing extensions
    "typing_extensions",
    # importlib.metadata (used by many packages)
    "importlib.metadata",
    "importlib_metadata",
    # aiohttp
    "aiohttp",
    "aiohttp.cookiejar",
    # requests/urllib3
    "requests",
    "urllib3",
    "certifi",
    "charset_normalizer",
    "idna",
]

for _pkg in [
    "streamlit",
    "webview",
    "altair",
    "pandas",
    "pyarrow",
    "aiohttp",
    "rich",
    "click",
    "tornado",
]:
    try:
        _d, _b, _h = collect_all(_pkg)
        extra_datas += _d
        extra_binaries += _b
        extra_hiddenimports += _h
    except Exception:
        pass  # optional / not installed — skip silently

# ── Analysis ───────────────────────────────────────────────────────────

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=extra_binaries,
    datas=[
        ("app", "app"),  # Streamlit pages, core modules, and .streamlit config
    ] + extra_datas,
    hiddenimports=extra_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# ── Build ──────────────────────────────────────────────────────────────

pyz = PYZ(a.pure)

# Resolve icon path — .icns on Mac, None on Windows (no custom icon)
_icon = "build_assets/icon.icns" if sys.platform == "darwin" else None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SafetyCulture Tools",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=_icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="SafetyCulture Tools",
)

# ── macOS .app bundle ──────────────────────────────────────────────────

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="SafetyCulture Tools.app",
        icon="build_assets/icon.icns",
        bundle_identifier="com.safetyculture.tools",
        info_plist={
            "CFBundleName": "SafetyCulture Tools",
            "CFBundleDisplayName": "SafetyCulture Tools",
            "CFBundleVersion": "1.0.0",
            "CFBundleShortVersionString": "1.0.0",
            "NSHighResolutionCapable": True,
        },
    )
