import io
from PIL import Image
from .chapter_image import ChapterImage


class PdfBuilder:
    def build(self, chapter_images: list[ChapterImage], reference_size: tuple[int, int] | None) -> bytes:
        if not chapter_images:
            return b""
        images: list[Image.Image] = []
        for ci in chapter_images:
            if ci.is_canvas and reference_size:
                ref_width = reference_size[0]
                ratio = ref_width / ci.image.width
                new_height = int(ci.image.height * ratio)
                images.append(ci.image.resize((ref_width, new_height), Image.Resampling.LANCZOS))
            else:
                images.append(ci.image)
        rgb_images = [im.convert("RGB") for im in images]
        pdf_buffer = io.BytesIO()
        rgb_images[0].save(pdf_buffer, save_all=True, append_images=rgb_images[1:], format="PDF")
        return pdf_buffer.getvalue()
