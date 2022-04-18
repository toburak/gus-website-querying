import requests
import json
import time
import numpy as np


sid = ''
class myClient:
  def __init__(self,Regon,Typ,Nazwa,KodPocztowy,Miejscowosc,Ulica,Numer_Nieruchomosci):
    self.regon = Regon
    self.typ = Typ
    self.nazwa = Nazwa
    self.kodpocztowy = KodPocztowy
    self.miejscowosc = Miejscowosc
    self.ulica = Ulica
    self.numernieruchomosci = Numer_Nieruchomosci

  @classmethod
  def from_json(cls, json_string):
    json_dict = json.loads(json_string)
    return cls(json_dict['Regon'],json_dict['Typ'],json_dict['Nazwa'],json_dict['KodPocztowy'],
        json_dict['Miejscowosc'],json_dict['Ulica'],json_dict['Numer_Nieruchomosci'])

  def __repr__(self):
    return f'<Client { self.nazwa }>'



class pkdPraw:
  def __init__(self,praw_pkdNazwa):
    self.pkdNazwa = praw_pkdNazwa

  @classmethod
  def from_json(cls, json_string):
    json_dict = json.loads(json_string)
    return cls(json_dict['praw_pkdNazwa'])

  def __repr__(self):
    return f'<pkdPraw { self.pkdNazwa }>'

class pkdFiz:
  def __init__(self,fiz_pkdNazwa):
    self.pkdNazwa = fiz_pkdNazwa

  @classmethod
  def from_json(cls, json_string):
    json_dict = json.loads(json_string)
    return cls(json_dict['fiz_pkdNazwa'])

  def __repr__(self):
    return f'<pkdFiz { self.pkdNazwa }>'

class myDetailsFiz:
  def __init__(self,fiz_nazwa,fiz_numerTelefonu,
              fiz_numerWewnetrznyTelefonu,fiz_numerFaksu,fiz_adresEmail,fiz_adresStronyinternetowej,
              fiz_nazwaPodstawowejFormyPrawnej,fiz_nazwaSzczegolnejFormyPrawnej):
    self.nazwa = fiz_nazwa
    self.numerTelefonu = fiz_numerTelefonu
    self.numerWewnetrznyTelefonu = fiz_numerWewnetrznyTelefonu
    self.numerFaksu = fiz_numerFaksu
    self.adresEmail = fiz_adresEmail
    self.adresStronyinternetowej = fiz_adresStronyinternetowej
    self.nazwaPodstawowejFormyPrawnej = fiz_nazwaPodstawowejFormyPrawnej
    self.nazwaSzczegolnejFormyPrawnej = fiz_nazwaSzczegolnejFormyPrawnej

  @classmethod
  def from_json(cls, json_string):
    json_dict = json.loads(json_string)
    return cls(json_dict['fiz_nazwa'],json_dict['fiz_numerTelefonu'],
        json_dict['fiz_numerWewnetrznyTelefonu'],json_dict['fiz_numerFaksu'],
        json_dict['fiz_adresEmail'],json_dict['fiz_adresStronyinternetowej'],
        json_dict['fiz_nazwaPodstawowejFormyPrawnej'],json_dict['fiz_nazwaSzczegolnejFormyPrawnej'])

  def __repr__(self):
    return f'<myDetailsFiz { self.fiz_nazwa }>'



class myDetailsPraw:
  def __init__(self,praw_nazwa,praw_numerTelefonu,
              praw_numerWewnetrznyTelefonu,praw_numerFaksu,praw_adresEmail,praw_adresStronyinternetowej,
              praw_nazwaPodstawowejFormyPrawnej,praw_nazwaSzczegolnejFormyPrawnej):

      self.nazwa = praw_nazwa
      self.numerTelefonu = praw_numerTelefonu
      self.numerWewnetrznyTelefonu = praw_numerWewnetrznyTelefonu
      self.numerFaksu = praw_numerFaksu
      self.adresEmail = praw_adresEmail
      self.adresStronyinternetowej = praw_adresStronyinternetowej
      self.nazwaPodstawowejFormyPrawnej = praw_nazwaPodstawowejFormyPrawnej
      self.nazwaSzczegolnejFormyPrawnej = praw_nazwaSzczegolnejFormyPrawnej

  @classmethod
  def from_json(cls, json_string):
    json_dict = json.loads(json_string)
    return cls(json_dict['praw_nazwa'],json_dict['praw_numerTelefonu'],
        json_dict['praw_numerWewnetrznyTelefonu'],json_dict['praw_numerFaksu'],
        json_dict['praw_adresEmail'],json_dict['praw_adresStronyinternetowej'],
        json_dict['praw_nazwaPodstawowejFormyPrawnej'],json_dict['praw_nazwaSzczegolnejFormyPrawnej'])

  def __repr__(self):
    return f'<myDetailsPraw { self.fiz_nazwa }>'

with open("nipy.csv") as file_name:
    myArray = np.loadtxt(file_name, delimiter=";")

url = "https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc/ajaxEndpoint/daneSzukaj"

headers = {
  'Connection': 'keep-alive',
  'sid': sid,
  'Content-type': 'application/json'
}


f = open('results.csv', 'w', encoding="utf-8")
f.write('nip;regon;nazwa;numerTelefonu;numerWewnetrzny;numerFaksu;adresEmail;adresStrony;nazwaPodstawowejFormyPrawnej;nazwaSzczegolnejFormyPrawnej;pkd;kodPocztowy;miejscowosc;ulica;numerNieruchomosci\n')

for onenip in myArray:
    payload = json.dumps({
    "pParametryWyszukiwania": {
        "Nip": onenip
    }
    })
    

    response = requests.request("POST", url, headers=headers, data=payload)
    myresponse = response.json() ['d']

    resp1 = myClient.from_json(myresponse[1:-1])



    url2 = "https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc/ajaxEndpoint/DanePobierzPelnyRaport"
    headers = {
      'Connection': 'keep-alive',
      'sid': sid,
      'Content-type': 'application/json'
    }
    
    time.sleep(0.4)
    if(resp1.typ=="P"):
      nazwaRaport = "DaneRaportPrawnaPubl"
      silos = 0
    else:
      nazwaRaport = "DaneRaportFizycznaPubl"
      silos = 1
    payload = json.dumps({
      "pRegon": resp1.regon,
      "pNazwaRaportu": nazwaRaport,
      "pSilosID": silos
    })
    #print(resp1.regon)
    response = requests.request("POST", url2, headers=headers, data=payload)
    myresponse2 = response.json() ['d']

    if(resp1.typ=="P"):
      resp2 = myDetailsPraw.from_json(myresponse2[1:-1])
    else:
      resp2 = myDetailsFiz.from_json(myresponse2[1:-1])
    #print(resp2.nazwa)
    
    time.sleep(0.4)

    #print(str(resp1.regon) + '00000')


    url3 = "https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc/ajaxEndpoint/DanePobierzPelnyRaport"
    headers = {
      'Connection': 'keep-alive',
      'sid': sid,
      'Content-type': 'application/json'
    }

    if(resp1.typ=="P"):
      nazwaRaport = "DaneRaportDzialalnosciPrawnejPubl"
      silos = 'undefined'
    else:
      nazwaRaport = "DaneRaportDzialalnosciFizycznejPubl"
      silos = 1
    payload = json.dumps({
      "pNazwaRaportu": nazwaRaport,
      "pRegon": str(resp1.regon) + '00000',
      "pSilosID": silos
    })
    response = requests.request("POST", url3, headers=headers, data=payload)
    myresponse3 = response.json() ['d']
    endOfFirstJSON = myresponse3.find('},{') + 1
    if(endOfFirstJSON>1):
      myresponse3 = myresponse3[1:endOfFirstJSON]
    else:
      myresponse3 = myresponse3[1:-1]
    if(resp1.typ=="P"):
      resp3 = pkdPraw.from_json(myresponse3)
    else:
      resp3 = pkdFiz.from_json(myresponse3)

    f.write(str(f'{onenip:10,.0f}'.replace(',', '')) + ';' + str(resp1.regon) + ';' + resp1.nazwa + ';' + str(resp2.numerTelefonu) + ';' + str(resp2.numerWewnetrznyTelefonu) + ';' + str(resp2.numerFaksu) + ';' + resp2.adresEmail + ';' + resp2.adresStronyinternetowej + ';' + resp2.nazwaPodstawowejFormyPrawnej + ';' + resp2.nazwaSzczegolnejFormyPrawnej + ';' + resp3.pkdNazwa + ';' + str(resp1.kodpocztowy) + ';' + resp1.miejscowosc + ';' + resp1.ulica + ';' + str(resp1.numernieruchomosci) + ';\n')
    
f.close()