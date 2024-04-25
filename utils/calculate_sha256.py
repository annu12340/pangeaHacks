import hashlib
from pathlib import Path

def calculate_sha256(file_name):
    BASE_DIR = Path(__file__).resolve().parent
    file_path = str(BASE_DIR / "media" / "reports" / file_name)  
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        sha256_hash = hashlib.sha256()
        while chunk := f.read(4096):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()