import requests
from os.path import exists
import os
from pathlib import Path
from tqdm import tqdm
import sys

#TODO: Figure out what to do about a progress bar.
from PyQt5.QtWidgets import QApplication, QLabel

    

def main():
    initialize()
    app = QApplication([])
    label = QLabel('Hello, World!')
    label.show()
    app.exec_()


def initialize():
    # Check to see if this sqlite database is not present.
    print("Checking to see if database.sqlite exists")
    blnDbFileExists = exists(os.getcwd() + '/database.sqlite')
    if not blnDbFileExists:
        url = 'https://mtgjson.com/api/v5/AllPrintings.sqlite'
        filesize = int(requests.head(url).headers["Content-Length"])
        filename = 'database.sqlite'

        # Code copied from the following github page: https://github.com/sirbowen78/lab/blob/master/file_handling/dl_file1.py
        with requests.get(url, stream=True) as r, open(os.getcwd() + '/database.sqlite','wb') as f, tqdm(
            unit="B",  # unit string to be displayed.
            unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
            unit_divisor=1024,  # is used when unit_scale is true
            total=filesize,  # the total iteration.
            file=sys.stdout,  # default goes to stderr, this is the display on console.
            desc=filename  # prefix to be displayed on progress bar.
        )   as progress:
                for chunk in r.iter_content(chunk_size=1024): 
                    # download the file chunk by chunk
                    datasize = f.write(chunk)
                    # on each chunk update the progress bar.
                    progress.update(datasize)


        #print("database.sqlite does not exist. Downloading...")
        #url = 'https://mtgjson.com/api/v5/AllPrintings.sqlite' #might need a better way to do this later to lock this down. 
        #file = requests.get(url)
        #writable = open(os.getcwd() + '/database.sqlite','wb').write(file.content)
    else:
        print("database.sqlite exists.")

    # Check to see if data from the sqlite is in the form that I wanted it to be in.
    print("Database table instantiation under construction.")
    # The form of this data will be done at a later date, as it will require a lot of experimentation with the data in question.
    # Would like to set up an s3 trigger or something that will mess with the data for me, 
    # so that from the application it can just download the preconfigured sqlite database.

main()