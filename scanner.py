import datetime
import time
import sys
import hashlib
import os

# The Shitty Little Scanner
# Author: Jake Headen
# Description: This is smaller scanner that can find things inside of file blobs, should work on disk images
# with a little bit of modifcation. Currently only finds the locations of JPG's but can easily be expanded
# to find any file signature you would want.

class Scanner:
    def __init__(self, fileName):
        self.fileName = fileName
        self.content = b''
    
    # Simple function, just reads in the contents as bytes
    def readFile(self):
        with open(self.fileName, 'rb') as f:
            self.content = f.read()
    
    
    # Looks and Confirms existence of JPG's
    # This needs a lot more work and splitting into more functions. On top of that will require
    # a nicer solution for searching large files and doing it all at once on something massive
    # will take a long time.
    def findJPG(self, extract = False):
        self.readFile() # Reading the file content in
        start = self.content.find(b'\xff\xd8\xff') # Looking for the generic JPG Header
        if start > 0: # If Successful
            end = self.content.find(b'\xff\xd9', start) # Looking for the trailer
            print("JPG Found")
            #print("Start: " + str(start))
            #print("End: " + str(end))
            if extract == True: # Optional to extract the images
                print("Extracting JPG")
                self.extractFile(start, end, '.jpg') # Extracts the image based on pos in the blob
    
    def findPNG(self, extract = False):
        self.readFile() # Reading the file content in
        start = self.content.find(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A') # Looking for the generic PNG Header
        if start > 0: # If Successful
            end = self.content.find(b'\x49\x45\x4E\x44\xAE\x42\x60\x82', start) # Looking for the trailer
            print("PNG Found")
            #print("Start: " + str(start))
            #print("End: " + str(end))
            if extract == True: # Optional to extract the images
                print("Extracting PNG")
                self.extractFile(start, end, '.png') # Extracts the image based on pos in the blob

    # Extracts Files
    # Could be cleaner
    def extractFile(self, start, end, trailer):
         img = self.content[start:end] # Gets the file content
         h = hashlib.sha256() 
         h.update(img) # Hashes the image content
         ts = time.time()
         directory = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d') # Folder with datestamp
         if not os.path.exists(directory):
            os.makedirs(directory)
         fname = directory + '/' + h.hexdigest() + trailer # Store using the hash
         with open(fname, 'wb') as f: # Writing bytes
             f.write(img)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Starting\n")
        scanner = Scanner(sys.argv[1])
        scanner.findJPG(True)
        scanner.findPNG(True)
