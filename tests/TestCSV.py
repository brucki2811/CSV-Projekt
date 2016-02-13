__author__ = "Bruckner Michael"
__version__ = 1.0
___date__ = 20160213

import unittest
from CSVUebung import *

class TestAllgemein(unittest.TestCase):

    def setUp(self):
        self.csvfile = csvwr("foo.csv")
        pass

    def test_csvFile(self):
        self.csvfile.read("blub.csv")
        self.csvfile.write("foo.csv")

    def test_dialects(self):
        self.csvfile.read("Dialects.csv")
        self.csvfile.write("foo.csv")

    def test_noneDialect(self):
        self.csvfile.read("blub.txt")
        self.csvfile.write("foo.csv")

if __name__ == "__main__":
    unittest.main()
