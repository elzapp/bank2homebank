#!/usr/bin/env python3
import csv
import datetime
class Transaction:
    def getDate(self):
        return self.date
    def getAmount(self):
        return self.amount
    def getPaymode(self):
        return self.paymode if hasattr(self,"paymode") else 0
    def getInfo(self):
        return self.info if hasattr(self,"info") else ""
    def getPayee(self):
        return self.payee if hasattr(self,"payee") else ""
    def getMemo(self):
        return self.memo if hasattr(self,"memo") else self.getInfo()
    def getCatetory(self):
        return self.category if hasattr(self,"category") else ""
    def getTagsString(self):
        return " ".join(self.tags) if hasattr(self,"tags") else ""
    def __repr__(self):
        return "Transaction(date='{}', amount='{}', info='{}'".format(self.date,self.amount,self.info)


aliases={
    "date":["BOKFØRINGSDATO","Bokføringsdato","Dato","Bokført"],
    "paymode":["TYPE","Tekstkode"],
    "info":["TEKST","Spesifikasjon","Forklaring","Beskrivelse"],
    "amount":["Beløp NOK","Beløp","INN PÅ KONTO","Inn på konto","Innskudd"],
    "amount_neg":["UT FRA KONTO","Ut av konto","Uttak"]}

def find_value(key,record):
    if key == "amount":
        for realkey in aliases["amount"]:
            if realkey in record and record[realkey] != "":
                return record[realkey].replace(",",".")
        for realkey in aliases["amount_neg"]:
            if realkey in record and record[realkey] != "":
                return "-"+record[realkey].replace(",",".")
    for realkey in aliases[key]:
        if realkey in record:
            return record[realkey]

def loadGeneric(path):
    with open(path, newline='',encoding="iso-8859-1") as csvfile:
        delimiter="\t"
        if ";" in csvfile.readline():
            delimiter=";"
        csvfile.seek(0)
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"')
        alldata=[e for e in reader if len(e)>0 and e[0] !=""]
        print(alldata[0])
        data=[dict(zip(alldata[0],e)) for e in alldata[1:]]
        r=[]
        for e in data:
            t=Transaction()
            t.amount=find_value("amount",e)
            t.info=find_value("info",e)
            t.category=find_value("paymode",e)
            if "-" in find_value("date",e):
                t.date=datetime.datetime.strptime(find_value("date",e),"%Y-%m-%d")
            else:
                t.date=datetime.datetime.strptime(find_value("date",e),"%d.%m.%Y")
            r.append(t)
        return r


def loadSkandiabanken(path):
    print("skandiabanken")
    paymodes={"Overføring":4, "Avtalegiro":8}
    r=[]
    with open(path, newline='',encoding="iso-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
        for row in reader:
            print(row)
            if(len(row)>=6 and row[0] != "" and row[1] != "RENTEDATO"):
              print(row)
              t=Transaction()
              t.date=datetime.datetime.strptime(row[0],"%Y-%m-%d")
              if row[5] != "":
                t.amount=float(row[5]) * -1.0
              if row[6] != "":
                t.amount=float(row[6]) * 1.0
              t.info=row[4]
              t.category=row[3]
              if t.category in paymodes:
                t.paymode=paymodes[t.category]
              r.append(t)
    return r

def loadFanaSparebank(path):
    print("Fana Sparebank")
    paymodes={"GEBYR":10,"GIRO":8,"VARER":1,"OVERFØRT":8,"OVFNETTB":4}
    r=[]
    with open(path, newline='',encoding="iso-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        mode="siste"
        for row in reader:
            if row[0] == "Dato":
                mode = "siste"
            elif row[1] == "Rentedato":
                mode = "arkiv"
            elif mode == "siste":
                print(row)
                t=Transaction()
                t.date=datetime.datetime.strptime(row[0],"%d.%m.%Y")
                t.info=row[1]
                if row[3] != "":
                  t.amount=row[3].replace(",",".")
                else:
                  t.amount="-"+row[2].replace(",",".")
                r.append(t)
            elif mode == "arkiv":
                print(row)
                t=Transaction()
                t.date=datetime.datetime.strptime(row[0],"%d.%m.%Y")
                t.info=row[3]
                t.amount = row[4].replace(",",".")
                t.category=row[2]
                r.append(t)
                if t.category in paymodes:
                  t.paymode=paymodes[t.category]
    return r

def loadSpv(path):
    print("Sparebanken Vest")
    r=[]
    with open(path, newline='',encoding="iso-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
        for row in reader:
            if row[0] != "Bokføringsdato" and row[0] != "Dato":
                print(row)
                t=Transaction()
                t.date=datetime.datetime.strptime(row[0],"%d.%m.%Y")
                t.info=row[1]
                t.amount=row[5]
                r.append(t)
    return r

def writeHomeBank(transactions, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f,delimiter=";")
        for t in transactions:
            ta=[]
            ta.append(t.getDate().strftime("%m-%d-%y"))
            ta.append(t.getPaymode())
            ta.append(t.getInfo())
            ta.append(t.getPayee())
            ta.append(t.getMemo())
            ta.append(t.getAmount())
            ta.append(t.getCatetory())
            ta.append(t.getTagsString())
            writer.writerow(ta)

handlers={
    "skandiabanken":loadSkandiabanken,
    "skb":loadSkandiabanken,
    "sparebankenvest":loadSpv,
    "spv":loadSpv,
    "fsb":loadFanaSparebank,
    "fanasparebank":loadFanaSparebank,
    "generic":loadGeneric
    }

if __name__ == "__main__":
    import sys
    (_,bank,src,dst) = sys.argv
    if bank in handlers:
        reader=handlers[bank]
        writeHomeBank(reader(src),dst)
    else:
        print("Sorry, no reader defined for \"{}\"".format(bank))
