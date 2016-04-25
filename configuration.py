
aliases={
    "date":["BOKFØRINGSDATO","BOKFÃ\x98RINGSDATO","Bokføringsdato","Dato","Bokført"],
    "paymode":["TYPE","Tekstkode"],
    "info":["TEKST","Spesifikasjon","Forklaring","Beskrivelse"],
    "amount":["Beløp NOK","Beløp","INN PÅ KONTO","Inn på konto","Innskudd"],
    "amount_neg":["UT FRA KONTO","Ut av konto","Uttak"]}

# From homebank:
# 0: None, 1: Kreditkort, 2: Sjekk, 3: Kontant, 4: Overfør,
# 5: Intern overfør, 6: Kreditt kort (?), 7: Standing order,
# 8: Elektronisk betaling, 9: Innskudd, 10: FI Fee, 11: Direct debit
paymodes={
    "GEBYR":10,"GIRO":8,"VARER":1,"OVERFØRT":8,"OVFNETTB":4,
    "Varekjøp":1,"Visa":1}


category={"AVTGI": "Giro","E-FAKTURA": "Giro"}
