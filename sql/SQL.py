__author__ = "Michael Bruckner"
__version__ = 1.0
__date__ = 20160309

from datetime import datetime
from orderedset.OrderedSet import OrderedSet
from sql.Connector import MySQLConnector

class SQL:
    def __init__(self, database, username, password, wahltermin):
        self.conn = MySQLConnector(username, password, database)
        self.wahltermin = wahltermin

    def writeList(self, datalist):
        ses = self.conn.getSession()

        ses.execute("DELETE FROM sprengelstimmen")
        ses.execute("DELETE FROM sprengel")
        ses.execute("DELETE FROM wahl")

        Wahl = self.conn.getClass("wahl")
        wahl = Wahl(termin=self.wahltermin, mandate=100)
        ses.add(wahl)

        Sprengel = self.conn.getClass("sprengel")
        Stimmabgabe = self.conn.getClass("sprengelstimmen")

        parteien = []
        for key in datalist[0].keys():
            if key not in ["SPR", "BZ", "WBER", "ABG.", "UNG.", "T", "WV", "WK"]:
                parteien.append(key)

        for column in datalist:
            sprengel = Sprengel(sprengelnr=int(column["SPR"]),
                                bezirknr=int(column["BZ"]),
                                termin=wahl.termin,
                                wahlberechtigte=int(column["WBER"]),
                                abgegebene=int(column["ABG."]),
                                ungueltige=int(column["UNG."]),
                                )
            ses.add(sprengel)
            for partei in parteien:
                stimmabgabe = Stimmabgabe(sprengelnr=int(column["SPR"]),
                                          bezirknr=int(column["BZ"]),
                                          termin=wahl.termin,
                                          abkuerzung=partei,
                                          anzahl=int(column[partei])
                                          )
                ses.add(stimmabgabe)

        ses.commit()

    def loadList(self):
        ses = self.conn.getSession()

        query = "SELECT wahlkreis.wnr, bezirk.bnr, sprengel.spnr, sprengel.wahlberechtigte, " \
                "sprengel.abgegebene, sprengel.ungueltige, sprengelstimmen.abkuerzung, sprengelstimmen.gueltige " \
                "FROM wahlkreis " \
                "INNER JOIN bezirk ON wahlkreis.wnr = bezirk.wnr " \
                "INNER JOIN sprengel ON bezirk.bnr = sprengel.bnr " \
                "AND sprengel.termin = '" + self.wahltermin + "' " \
                "INNER JOIN sprengelstimmen ON sprengelstimmen.termin = '" + self.wahltermin + "' " \
                "AND sprengelstimmen.bnr = bezirk.nr " \
                "AND sprengelstimmen.spnr = sprengel.spnr;"
        result = ses.execute(query).fetchall()

        header = OrderedSet(["WK", "BZ", "SPR", "WBER", "ABG.", "UNG."])
        datalist = []
        row = {}
        erstepartei = None
        for i in range(0, len(result)):
            abk = result[i]["abkuerzung"]
            if erstepartei is None or abk == erstepartei:
                if row:
                    datalist.append(row)
                column = {}
                erstepartei = abk
                column["WK"] = result[i]["wnr"]
                column["BZ"] = result[i]["bnr"]
                column["SPR"] = result[i]["spnr"]
                column["WBER"] = result[i]["wahlberechtigte"]
                column["ABG."] = result[i]["abgegebene"]
                column["UNG."] = result[i]["ungueltige"]
            row[abk] = result[i]["gueltige"]
            header.add(abk)

        return datalist, list(header)

    def results(self):

        termin = self.wahltermin
        zeitpunkt = datetime.now().time().strftime("%H:%M:%S")

        conn = self.conn.getConnection()
        cursor = conn.cursor()
        cursor.callproc("erstelleHochrechnung", [termin,zeitpunkt])
        cursor.close()
        conn.commit()

        ses = self.conn.getSession()
        ses.commit()
        query = "SELECT * FROM hochrechnungsdaten WHERE termin = '" + termin + "' AND zeitpunkt = '" + zeitpunkt + "';"
        result = ses.execute(query).fetchall()

        column = {}
        header = []
        datalist = []
        for i in range(0, len(result)):
            column[result[i]["abkuerzung"]] = result[i]["prozent"]
            header.append(result[i]["abkuerzung"])
        datalist.append(column)

        return datalist, header