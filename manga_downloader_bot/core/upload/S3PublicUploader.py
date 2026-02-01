import io
import os
import re
import zipfile
import boto3
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

BUCKET = os.getenv("BUCKET")
REGION = os.getenv("REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

class S3PublicUploader:
    def __init__(self):
        kwargs = {"region_name": REGION}
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

        self.client = boto3.client("s3", **kwargs)

    def upload_manga(self, manga_title: str, pdfs: list[bytes]) -> str:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for i, data in enumerate(pdfs):
                zf.writestr(f"{i + 1}.pdf", data)

        buf.seek(0)
        title_safe = re.sub(r'[\\/:*?"<>|\s]+', '_', manga_title).strip('_')
        key = f"{title_safe}.zip"
        
        self.client.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=buf.getvalue(),
            ContentType="application/zip",
        )
        
        return f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{quote(key)}"
