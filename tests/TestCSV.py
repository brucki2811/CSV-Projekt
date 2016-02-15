#!/usr/bin/env python3
import unittest
from csv_tool.CSVUebung import *

__author__ = "Bruckner Michael"
__version__ = 1.0
___date__ = 20160213

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
