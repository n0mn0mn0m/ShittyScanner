import datetime
import time
import sys
import hashlib
import os

class Scanner:
    def __init__(self, fileName):
        self.content = self.readFile(fileName)
        self.signatures = [
            # Just keep adding signatures here to expand the search list
            # type 0 == has header and trailer, 1 == size is in header
            # for type 1, header should be the first part of the header, trailer should be the part
            # that comes after the size byte(s)
            {'type' : '0', 'name' : 'JPEG', 'header' : b'\xff\xd8\xff', 'trailer' : b'\xff\xd9', 'extension' : '.jpg'},
            {'type' : '0', 'name' : 'PNG', 'header' : b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', 'trailer' : b'\x49\x45\x4E\x44\xAE\x42\x60\x82', 'extension' : '.png'},
            {'type' : '0', 'name' : 'MPEG2', 'header' : b'\x00\x00\x01\xBA', 'trailer' : '\x00\x00\x01\xB9', 'extension' : '.mpg'},
            {'type' : '0', 'name' : 'MPEG', 'header' : b'\x00\x00\x01', 'trailer' : '\x00\x00\x01\xB7', 'extension' : '.mpg'}

        ]
    
    def readFile(self, fileName):
        with open(fileName, 'rb') as f:
            content = f.read()
        return content
    
    # Extra IF needs adding to work with files that have no trailer but has the size in the header
    def scan(self, extract = False):
        for signature in self.signatures:
            start = 0
            end = 0
            while True:
                start = self.content.find(signature['header'], start + 1)
                if start > 0:
                    end = self.content.find(signature['trailer'])
                    if end > 0:
                        if signature['type'] == '1':  
                            end = int.from_bytes(self.content[start + len(signature['header']):end))
                            
                        print(signature['name'] + ' Found')
                        if extract == True:
                            self.extractFile(start, end, signature['extension'], signature['name']
                                
                else:
                    break
    
    def hashFile(self, content):
        h = hashlib.sha256() 
        h.update(content)
        return h.hexdigest()

    def createDirectory(self):
        ts = time.time()
        directory = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d') # Folder with datestamp
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def extractFile(self, start, end, ext, name):
        print('Extracting ' + name)
        content = self.content[start:end]
        fileHash = self.hashFile(content)
        directoryName = self.createDirectory()
        fileName = directoryName + '/' + fileHash + ext
        with open(fileName, 'wb') as f:
            f.write(content)
            print(name + ' Stored : ' + fileName) 

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scanner = Scanner(sys.argv[1])
        scanner.scan(True) # True to extract files
