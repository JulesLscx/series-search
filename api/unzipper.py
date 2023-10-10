import py7zr
import zipfile
import os
import re
from cleaner import Cleaner


class Unzipper:
    destination = None
    path_to_process = None
    def u_zip(self, path):
        if os.path.exists(path):
            self.path_to_process = path
        else:
            raise Exception("Path does not exists")
        if os.path.exists(self.destination):
            self.destination = destination
        else:
            raise Exception("Path does not exists")
        if os.path.exists(self.path_to_process):
            if self.path_to_process.endswith('.zip'):
                with zipfile.ZipFile(self.path_to_process, 'r') as zip_ref:
                    zip_ref.extractall(self.destination)
            elif self.path_to_process.endswith('.7z'):
                with py7zr.SevenZipFile(self.path_to_process, 'r') as zip_ref:
                    zip_ref.extractall(self.destination)
            else:
                raise Exception("File type not supported")
        else:
            raise Exception("Path does not exists")
        return self.destination
    
    def __init__(self, destination, path_to_process):
        if os.path.exists(destination):
            self.destination = destination
        else:
            raise Exception("Path does not exists")
    