


# Make this a class
import re
import os
class Cleaner:
    
    path_to_clean = None
    
    def __init__(self, path_to_clean):
        if os.path.exists(path_to_clean):
            self.path_to_clean = path_to_clean
        if path_to_clean == None or path_to_clean == '':
            return;
        else:
            raise Exception("Path does not exists")
        
    def set_path_to_clean(self, path_to_clean):
        if os.path.exists(path_to_clean):
            self.path_to_clean = path_to_clean
        else:
            raise Exception("Path does not exists")

    def clean(self):
        if os.path.isfile(self.path_to_clean):
            try :
                tmp = self.read_file(self.path_to_clean)
                return self.clean_text(tmp)
            except:
                return ''
        
    def clean_text(self, file):
        lines = []
    # Remove tags from .sub files
        for line in file.splitlines():
            line = line.strip()
            if line == '':
                continue
            if re.match(r'^[0-9]+$', line):
                continue
            if re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line):
                continue
            # Url pattern
            if re.match(r'^https?:\/\/.*[\r\n]*', line):
                continue
            if re.match(r'^www\..*[\r\n]*', line):
                continue
            # remove {number}{number} pattern
            if re.match(r'{\d+}{\d+}.*[\r\n]*', line):
                line = re.sub(r'{\d+}{\d+}', '', line)
                line = line.replace('|', ' ')
                # Remove ponctuation
                # Line containing html tags
            if re.match(r'^<.*>.*[\r\n]*', line):
                # remove html tags
                line = re.sub(r'<[^>]*>', '', line)
                # Remove closing tags
                line = re.sub(r'</[^>]*>', '', line)
            lines.append(line.strip())
            # Keep only ascii characters
        #Remove 3 first and 3 last lines of the file because they are most of the time publisher information
        text = ' '.join(lines[3:-3])
        return text
    
    def read_file(self, filename):
        with open(filename) as f:
            return f.read()
        