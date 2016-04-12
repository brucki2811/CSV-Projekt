author__ = 'Bruckner Michael'
__version__ = 1.2
__date__ = 20160325

from csv import DictReader, Sniffer, DictWriter
from PySide.QtGui import QMainWindow


class Model(object):
    def __init__(self, mainwindow):
        self.mainwindow = QMainWindow
        self.currentfile = None
        self.liste = []

    def read_csv(self, fname):
        with open(fname, 'r') as f:
            try:
                dialect = Sniffer().sniff(f.read(), ['\t', ';', ',', ' ', ':', '|'])
            except:
                dialect = None
            f.seek(0)
            csvreader = DictReader(f, dialect=dialect)

            for n in csvreader:
                self.liste.append(n)

        return self.liste, csvreader.fieldnames

    def write_csv(self, array, fname, delimiter=':'):
        with open(fname, 'w') as f:
            fieldnames = list(array[0].keys())
            writer = DictWriter(f, delimiter=delimiter, lineterminator='\n', fieldnames=fieldnames)
            writer.writerow(dict((field, field) for field in fieldnames))
            for row in array:
                writer.writerow(row)
