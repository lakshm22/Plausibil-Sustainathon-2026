def ocr_fallback_available():
    try:
        import pytesseract  # optional dependency
        return True
    except ImportError:
        return False

def ocr_page(_image):
    if not ocr_fallback_available():
        raise RuntimeError("Tesseract/PyTesseract is not installed.")
    import pytesseract
    return pytesseract.image_to_string(_image)
