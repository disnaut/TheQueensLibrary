from os.path import exists, dirname
import os
import requests
import hashlib
import sqlite3

# TODO: Add data validation that will throw exceptions based on what is thrown

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

def DeckTableExists(sqlDatabase):
    #include something to check for if there is more than one row. if there is more than one, there is a problem.
    sqlCursor = sqlDatabase.cursor()
    sqlCursor.execute('''SELECT EXISTS ( SELECT name FROM sqlite_schema WHERE type = 'table' AND name = 'Decks')''')
    sqlTuple = cur.fetchone()
    return sqlTuple[0];

def CardsInDeckTableExists(sqlDatabase):
    sqlCursor = sqlDatabase.cursor()
    sqlCursor.execute('''SELECT EXISTS ( SELECT name FROM sqlite_schema WHERE type = 'table' AND name = 'CardsInDeck')''')
    sqlTuple = cur.fetchone()
    return sqlTuple[0];

def InitUserSchema(sqlDatabase, intDeck, intCardsInDeck):
    sqlCursor = sqlDatabase.cursor()
    if inDeck == 0:
        sqlCursor.execute('''CREATE TABLE Deck(intDeckID INT PRIMARY KEY NOT NULL,  strDeckName TEXT NOT NULL, strFormat TEXT NOT NULL)''')
        sqlCursor.commit()
    if intCardsInDeck == 0:
        sqlCursor.execute('''CREATE TABLE Deck(intCardID INT PRIMARY KEY NOT NULL,  intDeckID INT NOT NULL, foreign key (intDeckID) references Decks (intDeckID) intNumOf INT NOT NULL)''')
        sqlCursor.commit()

def CopyUserSchema(sqlOldDatabase, sqlUserDatabase):
    print("Under Construction.")
    return False

## TODO: Fix where these files are downloaded, and determine how to keep the
##       pwd in the root of this project.

# Quick and dirty fix: Run a module after this that moves the files in question. (sub optimal)
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

    #If the file does not exist, or there is a new database, download and overwrite the old database
    ## TODO: Develop a solution to losing user data when this download is occuring
    if FileExists('MTG_Database.sqlite') == False or blnNewDatabase:
        DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite', 'MTG_Database.sqlite')

    #Create a sqlite connection to the datbase
    sqlDatabase = sqlite3.connect('MTG_Database.sqlite')

    #Check if tables exist
    intDeckExists = DeckTableExists(sqlDatabase)
    intCardsInDeckExists = CardsInDeckTableExists(sqlDatabase)
    InitUserSchema(sqlDatabase, intDeckExists, intCardsInDeck)
main()
