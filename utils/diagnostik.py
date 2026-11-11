"""Diagnostik lingkungan: periksa modul yang dibutuhkan aplikasi dan modul opsional (PDF, grafik, QR).
Jalankan di terminal:  python -m utils.diagnostik"""
from __future__ import annotations

import importlib
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import Dict, List

# (modul, paket pip, wajib?)
MODUL = [
    ("streamlit", "streamlit", True), ("pandas", "pandas", True), ("numpy", "numpy", True),
    ("plotly.graph_objects", "plotly", False), ("PIL", "pillow", False),
    ("reportlab.platypus", "reportlab", False), ("reportlab.pdfgen.canvas", "reportlab", False),
    ("reportlab.graphics.barcode.qr", "reportlab", False),
]


def periksa_modul() -> List[Dict]:
    hasil = []
    for modul, paket, wajib in MODUL:
        try:
            importlib.import_module(modul)
            try:
                v = version(paket)
            except PackageNotFoundError:
                v = "?"
            hasil.append(dict(modul=modul, ok=True, versi=v, wajib=wajib, galat=""))
        except Exception as e:
            hasil.append(dict(modul=modul, ok=False, versi="-", wajib=wajib, galat=f"{type(e).__name__}: {e}"))
    return hasil


def info_python() -> str:
    return f"Python {platform.python_version()} ({platform.system()} {platform.machine()})"


def ringkasan() -> str:
    baris = [info_python()] + [f"{'OK ' if h['ok'] else 'GAGAL'} {h['modul']:<32} {h['versi']:<10} {h['galat']}" for h in periksa_modul()]
    return "\n".join(baris)


if __name__ == "__main__":
    print(ringkasan())
    sys.exit(0 if all(h["ok"] for h in periksa_modul() if h["wajib"]) else 1)
