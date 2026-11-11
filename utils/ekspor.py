"""Pembuat dokumen yang TIDAK melempar galat: kegagalan satu format (mis. reportlab bermasalah di server) tidak merusak aplikasi.
Setiap fungsi mengembalikan (hasil, pesan_galat); salah satunya None."""
from __future__ import annotations

from typing import Optional, Tuple


def _aman(fungsi, dok, nama: str):
    try:
        return fungsi(dok), None
    except Exception as e:                      # termasuk ImportError / ModuleNotFoundError dari pustaka
        return None, f"{nama} tidak dapat dibuat: {type(e).__name__}: {e}"


def pdf(dok) -> Tuple[Optional[bytes], Optional[str]]:
    from utils.laporan_pdf import buat_pdf
    return _aman(buat_pdf, dok, "PDF")


def docx(dok) -> Tuple[Optional[bytes], Optional[str]]:
    from utils.laporan_docx import buat_docx
    return _aman(buat_docx, dok, "Word")


def html(dok) -> Tuple[Optional[str], Optional[str]]:
    from utils.laporan_html import buat_html
    return _aman(buat_html, dok, "HTML")
