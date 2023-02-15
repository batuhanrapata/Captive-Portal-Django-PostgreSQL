import requests
import xmltodict


def kps(name, surname, tc_no, birth_date):
    url = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
    payload = f"""<?xml version="1.0" encoding="utf-8"?> 
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
          <TCKimlikNo>{tc_no}</TCKimlikNo>
          <Ad> {name}</Ad>
          <Soyad> {surname}</Soyad>
          <DogumYili>{birth_date}</DogumYili>
        </TCKimlikNoDogrula> 
      </soap:Body>
    </soap:Envelope>"""
    headers = {'content-type': 'text/xml'}
    response = requests.post(url, data=payload, headers=headers)
    resp = xmltodict.parse(response.content)
    return resp['soap:Envelope']['soap:Body']['TCKimlikNoDogrulaResponse']['TCKimlikNoDogrulaResult'] == 'true'
