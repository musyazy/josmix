"""Ketahanan: aplikasi tetap berjalan bila reportlab / reportlab.graphics / Pillow bermasalah (mis. di server cloud)."""
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KODE = """
import sys
BLOK = {blok!r}
for nama in BLOK:
    sys.modules[nama] = None          # import modul ini sekarang melempar ModuleNotFoundError
sys.path.insert(0, {root!r}); sys.path.insert(0, {tests!r})
import utils.laporan_pdf, utils.laporan_html, utils.laporan_docx, utils.ekspor, utils.dokumen, utils.charts, utils.diagnostik
from helpers import KOP, bundle_uji, lab_uji
from utils.dokumen import bangun_laporan
from utils import ekspor
lab = lab_uji(); dok = bangun_laporan(KOP, lab, bundle_uji(lab, True))
pdf, g_pdf = ekspor.pdf(dok); word, g_word = ekspor.docx(dok); html, g_html = ekspor.html(dok)
print("PDF", pdf is not None and pdf[:5] == b"%PDF-", "|", (g_pdf or "")[:60])
print("DOCX", word is not None and word[:2] == b"PK", "|", (g_word or "")[:60])
print("HTML", html is not None and "<html" in html, "|", (g_html or "")[:60])
"""


def _jalankan(blok):
    r = subprocess.run([sys.executable, "-c", KODE.format(blok=blok, root=ROOT, tests=os.path.join(ROOT, "tests"))],
                       capture_output=True, text=True, cwd=ROOT, timeout=120)
    assert r.returncode == 0, r.stderr[-800:]
    return r.stdout


def test_normal():
    o = _jalankan([])
    assert "PDF True" in o and "DOCX True" in o and "HTML True" in o


def test_tanpa_reportlab_graphics_pdf_tetap_dibuat():
    """Kasus di cloud: sub-modul grafis/QR reportlab tidak bisa diimpor. PDF memakai kanvas inti (tanpa grafis) dan QR dilewati."""
    o = _jalankan(["reportlab.graphics", "reportlab.graphics.shapes", "reportlab.graphics.barcode", "reportlab.graphics.barcode.qr"])
    assert "PDF True" in o and "DOCX True" in o and "HTML True" in o


def test_tanpa_reportlab_sama_sekali_aplikasi_tetap_hidup():
    o = _jalankan(["reportlab"])
    assert "PDF False" in o and "tidak dapat dibuat" in o        # PDF gagal terkendali
    assert "DOCX True" in o and "HTML True" in o                 # format lain tetap jalan


def test_tanpa_pillow_word_tetap_dibuat_tanpa_gambar():
    o = _jalankan(["PIL"])
    assert "DOCX True" in o and "HTML True" in o
