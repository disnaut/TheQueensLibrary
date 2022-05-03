import pytest
from ..\modules.DatabaseInit import *

def test_HashFile_Does_Not_Exist():
    assert FileExists('AllPrintings.sqlite.sha256') == False

def test_HashFile_Download():
    assert DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite.sha256') == True

def test_HashFile_Exists():
    assert FileExists('AllPrintings.sqlite.sha256') == True

def test_Database_Does_Not_Exist():
    assert FileExists('MTG_Database.sqlite') == False

def test_Database_Download():
    assert DownloadFile('https://mtgjson.com/api/v5/AllPrintings.sqlite') == True

def test_Database_Exists():
    assert FileExists('MTG_Database.sqlite') == True

def test_HashFile_Compared_To_Database_Hash():
    assert HashCompare('MTG_Database.sqlite')

def test_HashFile_Compared_To_Other_File():
    assert HashCompare('Test.txt')
