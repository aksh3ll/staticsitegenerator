import os
import shutil
import logging

logger = logging.getLogger(__name__)

def clear_directory(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)

def copy_static_files(src: str, dest: str):
    if not os.path.exists(dest):
        os.mkdir(dest)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isfile(s):
            shutil.copy(s, d)
        elif os.path.isdir(s):
            copy_static_files(s, d)
