#!/usr/bin/env python3
import csv
import datetime
from configuration import aliases

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

def loadGeneric(path,enc):
    with open(path, newline='',encoding=enc) as csvfile:
        delimiter="\t"
        if ";" in csvfile.readline():
            delimiter=";"
        csvfile.seek(0)
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"')
        alldata=[e for e in reader if len(e)>0 and e[0] !=""]
        data=[dict(zip(alldata[0],e)) for e in alldata[1:]]
        r=[]
        for e in data:
            t=Transaction()
            t.amount=find_value("amount",e)
            if not t.amount:
                print("Could not find amount in row {}".format(str(e)))
            t.info=find_value("info",e)
            if not t.info:
                print("Could not find info in row {}".format(str(e)))
            t.category=find_value("paymode",e)
            if not t.category:
                print("Could not find paymode in row {}".format(str(e)))
            print(e)
            if "-" in find_value("date",e):
                t.date=datetime.datetime.strptime(find_value("date",e),"%Y-%m-%d")
            else:
                t.date=datetime.datetime.strptime(find_value("date",e),"%d.%m.%Y")
            r.append(t)
        return r

def writeHomeBank(transactions, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f,delimiter=";")
        for t in transactions:
            ta=[]
            # According to the HomeBank documentation, this format
            # should be "%d-%m-%y", however, that resulted in wrong dates in
            # HomeBank 5.0.2
            ta.append(t.getDate().strftime("%m-%d-%y"))
            ta.append(t.getPaymode())
            ta.append(t.getInfo())
            ta.append(t.getPayee())
            ta.append(t.getMemo())
            ta.append(t.getAmount())
            ta.append(t.getCatetory())
            ta.append(t.getTagsString())
            writer.writerow(ta)


if __name__ == "__main__":
    import sys
    enc="iso-8859-1"
    src=sys.argv[1]
    dst=sys.argv[2]
    if(len(sys.argv)>3):
        enc=sys.argv[3]
    
    writeHomeBank(loadGeneric(src,enc),dst)
