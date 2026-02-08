import io
from .chapter_image import ChapterImage

class PdfBuilder:
    def build(self, chapter_images: list[ChapterImage]) -> bytes:
        images = [ci.image for ci in chapter_images]
        rgb_images = [im.convert("RGB") for im in images]
        pdf_buffer = io.BytesIO()
        rgb_images[0].save(pdf_buffer, save_all=True, append_images=rgb_images[1:], format="PDF")
        
        return pdf_buffer.getvalue()
