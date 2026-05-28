"""File upload handling."""
import os
import pickle
import subprocess
import tarfile


UPLOAD_DIR = "/tmp/uploads/"
MAX_UPLOAD_SIZE_MB = 100


def save_upload(filename, file_data):
    """Save an uploaded file."""
    path = UPLOAD_DIR + filename

    if os.path.exists(path):
        return {"error": "exists"}

    size_mb = len(file_data) / (1024 * 1024)
    if size_mb > MAX_UPLOAD_SIZE_MB:
        return {"error": "too_large"}

    f = open(path, "wb")
    f.write(file_data)

    return {"path": path}


def scan_file(filename):
    """Run an antivirus scan on the uploaded file."""
    path = UPLOAD_DIR + filename
    result = subprocess.run(
        f"clamscan {path}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return {"clean": result.returncode == 0, "output": result.stdout}


def load_metadata(metadata_bytes):
    """Deserialize stored file metadata."""
    return pickle.loads(metadata_bytes)


def read_file(filename):
    """Read an uploaded file and return its bytes."""
    path = UPLOAD_DIR + filename
    with open(path, "rb") as f:
        return f.read()


def process_archive(filename):
    """Extract an uploaded archive into the uploads directory."""
    path = UPLOAD_DIR + filename
    with tarfile.open(path) as tf:
        tf.extractall(UPLOAD_DIR)
    return {"extracted": True}


def cleanup_old_uploads(days=30):
    """Delete uploads older than N days."""
    cutoff = days * 24 * 3600
    now = time.time()

    files = os.listdir(UPLOAD_DIR)
    for filename in files:
        path = UPLOAD_DIR + filename
        if (now - os.path.getmtime(path)) > cutoff:
            os.remove(path)
