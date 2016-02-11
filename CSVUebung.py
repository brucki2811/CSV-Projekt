__author__ = "Bruckner Michael"
__version__ = 1.0
___date__ = 20160122
"""
Die Klasse csvwr ermoeglicht uns das Lesen von Daten und das Schreiben von diesen.
Es ist moeglich Daten aus anderen Files zusaetzlich anzuhaengen.
"""
import csv

class csvwr(object):

    def __init__(self, file):
        self.file = file
        self.liste = []

    """
    Mittels der Methode read koennen wir jedes beliebige File einlesen.
    """
    def read(self,filename):
        with open(filename, 'r') as f:
            try:
                dialect = csv.Sniffer().sniff(f.read(), [',', '\t', ';', ' ', ':', '|'])
            except:
                dialect = None
            f.seek(0)
            csvreader = csv.reader(f, dialect)

            for n in csvreader:
                self.liste.append(n)

        return self.liste

    """
    Mittels der Methode write koennen wir jedes beliebige File schreiben.
    """
    def write(self,filename):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.liste)


csvfile = csvwr("sprengel.csv")
csvfile.read("sprengel.csv")
csvfile.write("test.csv")
csvfile.read("test1.csv")
csvfile.write("test.csv")