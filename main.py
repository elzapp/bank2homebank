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
        return self.memo if hasattr(self,"memo") else ""
    def getCatetory(self):
        return self.category if hasattr(self,"category") else ""
    def getTagsString(self):
        return " ".join(self.tags) if hasattr(self,"tags") else ""
    def __repr__(self):
        return "Transaction(date='{}', amount='{}', info='{}'".format(self.date,self.amount,self.info)


def loadSkandiabanken(path):
    paymodes={"Overføring":4, "Avtalegiro":8}
    r=[]
    with open(path, newline='',encoding="iso-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
        for row in reader:
            if(len(row)>=6 and row[0] != "" and row[1] != "RENTEDATO"):
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


def loadSpv(path):
    r=[]
    with open(path, newline='',encoding="iso-8859-1") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
        for row in reader:
            if row[0] != "Bokføringsdato":
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
            ta.append(t.getDate().strftime("%d-%m-%y"))
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
    "spv":loadSpv
    }

if __name__ == "__main__":
    import sys
    (_,bank,src,dst) = sys.argv
    if bank in handlers:
        reader=handlers[bank]
        writeHomeBank(reader(src),dst)
    else:
        print("Sorry, no reader defined for \"{}\"".format(bank))
