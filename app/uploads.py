"""File upload handling."""
import os
import pickle


UPLOAD_DIR = "/tmp/uploads/"


def save_upload(filename, file_data):
    """Save an uploaded file."""
    path = UPLOAD_DIR + filename

    if os.path.exists(path):
        return {"error": "exists"}

    f = open(path, "wb")
    f.write(file_data)

    return {"path": path}


def load_metadata(metadata_bytes):
    """Deserialize stored file metadata."""
    return pickle.loads(metadata_bytes)


def read_file(filename):
    """Read an uploaded file and return its bytes."""
    path = UPLOAD_DIR + filename
    with open(path, "rb") as f:
        return f.read()


def cleanup_old_uploads(days=30):
    """Delete uploads older than N days."""
    cutoff = days * 24 * 3600
    now = time.time()

    files = os.listdir(UPLOAD_DIR)
    for filename in files:
        path = UPLOAD_DIR + filename
        if (now - os.path.getmtime(path)) > cutoff:
            os.remove(path)
