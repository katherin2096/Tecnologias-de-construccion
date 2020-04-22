import http.client
api = http.client.HTTPSConnection("linguatools-conjugations.p.rapidapi.com")

headers = {    
    'x-rapidapi-host': "linguatools-conjugations.p.rapidapi.com",
    'x-rapidapi-key': "961105f553msh1e8effe69ef2988p11f182jsn1f28601f3fb3"
}


ruta='palabras.txt'
link="/conjugate/?verb="
archivo=open(ruta,'r')
txt='.txt'
for linea in archivo:
    palabra=linea.strip()
    fichero=open(palabra+txt,'w')
    api.request("GET", link+palabra, headers=headers)
    res = api.getresponse()
    data = res.read()
    datos=str(data, 'utf-8')
    fichero.write(datos)
