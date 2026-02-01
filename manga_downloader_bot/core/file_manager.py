import os
import shutil
from PIL import Image

MANGAS_FOLDER_NAME = 'mangas'

class FileManager:
    def create_folder(self, folder_name: str):
        manga_path = self._get_manga_path()
        os.makedirs(manga_path, exist_ok=True)

        folder_path = os.path.join(manga_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    def save_img(self, manga_title: str, img_name: str, img: bytes):
        img_path = os.path.join(self._get_manga_path(), manga_title, img_name)

        with open(img_path, "wb") as f:
            f.write(img)

    def save_img_pil(self, manga_title: str, img_name: str, img: Image):
        img_path = os.path.join(self._get_manga_path(), manga_title, img_name)

        img.save(img_path)

    def create_pdf(self, manga_title: str, chapter_name: str) -> str | None:
        folder_path = os.path.join(self._get_manga_path(), manga_title)
        images = []
        
        imgs = [i for i in os.listdir(folder_path) if i.endswith('.png')]

        for i in range(len(imgs)):
            img_path = os.path.join(folder_path, f'{i}.png')
            images.append(Image.open(img_path))

        if images:
            pdf_path = os.path.join(folder_path, f'{chapter_name}.pdf')
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
            return pdf_path
        
        return None
    
    def clean_images(self,  manga_title: str):
        folder_path = os.path.join(self._get_manga_path(), manga_title)

        for img in os.listdir(folder_path):
            if img.endswith('.png'):
                os.remove(os.path.join(folder_path, img))
    
    def clean_folder(self,  manga_title: str):
        folder_path = os.path.join(self._get_manga_path(), manga_title)

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    def _get_manga_path(self) -> str:
        module_root = os.path.dirname(os.path.abspath(__file__))
        manga_path = os.path.join(module_root, MANGAS_FOLDER_NAME)
        return manga_path