import pytest
import sys
import os
#This is to make sure that the modules are imported correctly.
#This directly modifies your python path. This may have to be
#changed because of security.
os.chdir(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.getcwd() + '/modules')
from DatabaseInit import *

## TODO: Change to False after I've set up the inner function logic
def test_HashFile_Does_Not_Exist():
    assert FileExists('AllPrintings.sqlite.sha256') == True

def test_HashFile_Download():
    assert DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite.sha256') == True

def test_HashFile_Exists():
    assert FileExists('AllPrintings.sqlite.sha256') == True

## TODO: Change to False after I've set up the inner function logic
def test_Database_Does_Not_Exist():
    assert FileExists('MTG_Database.sqlite') == True

def test_Database_Download():
    assert DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite') == True

def test_Database_Exists():
    assert FileExists('MTG_Database.sqlite') == True

def test_HashFile_Compared_To_Database_Hash():
    assert HashCompare('MTG_Database.sqlite')

def test_HashFile_Compared_To_Other_File():
    assert HashCompare('Test.txt')
