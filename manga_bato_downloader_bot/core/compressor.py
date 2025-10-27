import shutil
import os

MANGAS_FOLDER_NAME = 'mangas'

class Compressor:
    def compress_folder(self, folder_name, archive_name) -> str:
        module_root = os.path.dirname(os.path.abspath(__file__))

        folder_path = os.path.join(module_root, MANGAS_FOLDER_NAME, folder_name)
        archive_path = os.path.join(module_root, MANGAS_FOLDER_NAME, archive_name)

        shutil.make_archive(archive_path, 'zip', folder_path)

        return archive_path + '.zip'