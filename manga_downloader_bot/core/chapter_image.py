from dataclasses import dataclass
from PIL import Image


@dataclass
class ChapterImage:
    image: Image.Image
    is_canvas: bool
