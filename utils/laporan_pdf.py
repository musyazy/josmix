"""Fasad PDF: memuat implementasi reportlab hanya saat dibutuhkan, sehingga masalah pada reportlab (mis. di server cloud)
tidak menjatuhkan seluruh aplikasi. Gunakan utils.ekspor.pdf(dok) untuk pemanggilan yang tidak melempar galat."""
from __future__ import annotations


class PdfTidakTersedia(RuntimeError):
    """reportlab tidak dapat dimuat atau pembuatan PDF gagal."""


def buat_pdf(dok) -> bytes:
    try:
        from utils import _pdf_reportlab as impl
    except ImportError as e:                       # ModuleNotFoundError adalah turunan ImportError
        raise PdfTidakTersedia(f"Modul PDF (reportlab) tidak dapat dimuat: {e}") from e
    return impl.buat_pdf(dok)


def tersedia() -> bool:
    try:
        from utils import _pdf_reportlab  # noqa: F401
        return True
    except ImportError:
        return False
