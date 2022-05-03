from os.path import exists, dirname
import os
import requests
import hashlib

def FileExists(strFileName):
    return exists(os.getcwd() + '/' + strFileName)

def DownloadFile(strDownloadUrl, strFileName):
    try:
        fileIn = requests.get(strDownloadUrl)
        fileOut = open(os.getcwd() + '/' + strFileName,'wb').write(fileIn.content)
        fileIn.close()
        return True
    except Exception as e:
        print(e)
        return False

def HashCompare(strFileName):
    strDownloadedDatbaseHash = LoadHashFile()
    strCalculatedHash = CalculateHash(strFileName)
    return strDownloadedDatbaseHash == strCalculatedHash

def LoadHashFile():
    fileIn = open('MTG_Database.sqlite.sha256', 'r')
    strHash = fileIn.readline().strip()
    fileIn.close()
    return strHash

def CalculateHash(strFileName):
    strHash = ''
    with open(strFileName,'rb') as f:
        bytes = f.read()
        strHash = hashlib.sha256(bytes).hexdigest()
    f.close()
    return strHash

def main():
    blnNewDatabase = False
    #Download the hash file, keep the name
    DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite.sha256', 'AllPrintings.sqlite.sha256')
    #Check to see if a hash file already exists
    if FileExists('MTG_Database.sqlite.sha256') == False:
    #If it does not exist, make the downloaded hash file the current hash file
        os.rename('AllPrintings.sqlite.sha256', 'MTG_Database.sqlite.sha256')
    else:
    #If it exists, compare the hashes
        if HashCompare('AllPrintings.sqlite.sha256') == False:
            os.remove('MTG_Database.sqlite.sha256')
            os.rename('AllPrintings.sqlite.sha256', 'MTG_Database.sqlite.sha256')
            blnNewDatabase = True

    #If the file does not exist, or
    if FileExists('MTG_Database.sqlite') == False or blnNewDatabase:
        DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite', 'MTG_Database.sqlite')

main()
