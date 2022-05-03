import pytest
import sys
import os
import time
#This is to make sure that the modules are imported correctly.
#This directly modifies your python path. This may have to be
#changed because of security.
os.chdir(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.getcwd() + '/modules')
from DatabaseInit import *

def BeforeTest():

    #The insanity below is because windows likes to open files again for an arbitary reason,
    #even after you have closed them for a given duration.
    #Please leave this alone until I can find a more elegant solution
    # - Damien
    while(os.path.exists(os.getcwd() + '/' + 'MTG_Database.sqlite.sha256') or os.path.exists(os.getcwd() + '/' + 'MTG_Database.sqlite')):
        time.sleep(2)
        try:
            if os.path.exists(os.getcwd() + '/' + 'MTG_Database.sqlite.sha256'):
                os.remove('MTG_Database.sqlite.sha256')
            if os.path.exists(os.getcwd() + '/' + 'MTG_Database.sqlite'):
                os.remove('MTG_Database.sqlite')
        except Exeception as e:
            print(e)

BeforeTest()

def test_HashFile_Does_Not_Exist():
    assert FileExists('MTG_Database.sqlite.sha256') == False

def test_Database_Does_Not_Exist():
    assert FileExists('MTG_Database.sqlite') == False

def test_HashFile_Download():
    assert DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite.sha256', 'MTG_Database.sqlite.sha256') == True

def test_Database_Download():
    assert DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite', 'MTG_Database.sqlite') == True


def test_HashFile_Exists():
    assert FileExists('MTG_Database.sqlite.sha256') == True

def test_Database_Exists():
    assert FileExists('MTG_Database.sqlite') == True

def test_HashFile_Compared_To_Database_Hash():
    assert HashCompare('MTG_Database.sqlite') == True

def test_HashFile_Compared_To_Other_File():
    assert HashCompare('Test.txt') == False
