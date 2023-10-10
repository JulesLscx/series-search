import py7zr
import zipfile
import os
import re
from cleaner import Cleaner


class Unzipper:
    destination = None
    path_to_process = None
    def u_zip(self, path):
        if (not os.path.exists(path)):
            raise Exception("Path does not exists")
        else:
            with py7zr.SevenZipFile(path, mode='r') as z:
                z.extractall()
        return True
    
    def __init__(self, destination, path_to_process):
        if os.path.exists(destination):
            self.destination = destination
        else:
            raise Exception("Path does not exists")
        
        
    def file_categoriser(self, folderName, fileName):
        dic = {}
        folderName = folderName.replace(' ', '')
        folderName = folderName.lower()
        fileName.replace(' ', '')
        fileName = fileName.lower()
        fileName = fileName.replace(' ', '').lower()
        fileName.replace(folderName, '')
        # Pattern = folderName + 'S' or 's' + seasonNumber + 'E' or 'e' + episodeNumber + 'VO' or 'VF' + '.srt'
        season = re.search(r'[Ss]\d+', fileName).group()
        if season == None:
            season = re.search(r'\d+x', fileName).group()
        episode = re.search(r'[Ee]\d+', fileName).group()
        if episode == None:
            episode = re.search(r'x\d+', fileName).group()
        language = re.search(r'[vef][ofnr]', fileName).group()
        if language == 'EN':
            language = 'VO'
        if language == 'FR':
            language = 'VF'

        dic['season'] = season
        dic['episode'] = episode
        dic['language'] = language
        return dic
    
    def find_serie(self, dirs):
        is_next = False
        for directory in dirs:
            if directory == 'sous-titres':
                is_next = True
                continue
            if is_next:
                return directory
        return None
    
    def unzip_all(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.zip'):
                    # Unzip the file here
                    try:
                        with zipfile.ZipFile(file_path, 'r') as z:
                            z.extractall(file_path[:-4])
                    except:
                        print('Error with ' + file_path)
                        continue
                elif file.endswith('.7z'):
                    # Unzip the file here
                    try:
                        with py7zr.SevenZipFile(file_path, mode='r') as z:
                            z.extractall(file_path[:-3])
                    except:
                        print('Error with ' + file_path)
                        continue
                    
    def categorise_all_sub(self, path, path_to_move):
        self.unzip_all(path)
        cleaner = Cleaner()
        os.makedirs(path_to_move, exist_ok=True)
        for folder in os.listdir(path=path):
            if os.path.isdir(path + os.sep + folder):
                print(folder)
                serie = folder
                path_to_copy = os.path.join(
                    path_to_move, serie)
                os.makedirs(path_to_copy, exist_ok=True)
            else:
                continue
            for root, dirs, files in os.walk(os.path.join(path, serie), topdown=False):
                print(root)
                for file in files:
                    if file.endswith('.srt') or file.endswith('.sub'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r') as f:
                                text = f.read()
                        except:
                            try:
                                with open(file_path, 'r', encoding="utf-8") as f:
                                    text = f.read()
                            except:
                                print('Error with ' + file_path)
                                continue
                        cleaner.set_path_to_clean(file_path)
                        clean_subs = cleaner.clean()
                        new_path = path_to_copy + os.sep + file[:-4] + '.txt'
                        with open(new_path, 'w', encoding="utf-8") as f:
                            f.write(clean_subs)
                    else:
                        continue