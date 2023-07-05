import urllib.parse
import requests
from datetime import datetime, timezone

main_api = "https://www.mapquestapi.com/directions/v2/route?"
clave = "p2smZqQ4ahyxnZj1ays7gjCWNz98wIzH"
translation_api = "https://api.mymemory.translated.net/get?"

def translate_text(text, target_language):
    url = translation_api + urllib.parse.urlencode({"q": text, "langpair": "en|" + target_language})
    response = requests.get(url).json()
    if "responseStatus" in response and response["responseStatus"] == 200:
        return response["responseData"]["translatedText"]
    else:
        return None

while True:
    orig = input("Ubicación inicial: ")
    if orig == "quit" or orig == "s":
        break
    dest = input("Destino: ")
    if dest == "quit" or dest == "s":
        break
    num_viajeros = int(input("Cantidad de viajeros: "))
    viajeros = []
    for i in range(num_viajeros):
        nombre = input("Nombre del viajero {}: ".format(i+1))
        viajeros.append(nombre)
    url = main_api + urllib.parse.urlencode({"key": clave, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    print("URL:" + url)
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("Estado de la API: " + str(json_status) + " = Consulta de ruta exitosa.\n")
        print("=============================================")
        print("Direcciones desde " + orig + " hasta " + dest)
        print("Duración del viaje: " + json_data["route"]["formattedTime"])
        print("Kilómetros: " + str("{:.1f}".format(json_data["route"]["distance"] * 1.61)))
        if "fuelUsed" in json_data["route"]:
            print("Combustible utilizado (L): " + str("{:.1f}".format(json_data["route"]["fuelUsed"] * 3.78)))
        else:
            print("No se pudo obtener la información de combustible utilizado.")
        santiago_time = datetime.now(timezone.utc).astimezone()
        print("Fecha y hora del reporte en Santiago, Chile: " + santiago_time.strftime("%Y-%m-%d %H:%M:%S"))
        print("=============================================")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            narrative = each["narrative"]
            # Traducción del texto al español utilizando la API de MyMemory
            translated_text = translate_text(narrative, "es")
            if translated_text is not None:
                print(translated_text + " (" + str("{:.2f}".format(each["distance"] * 1.61)) + "km)")
            else:
                print(narrative + " (" + str("{:.2f}".format(each["distance"] * 1.61)) + "km)")
        print("=====================================================\n")
        print("Nombres de los viajeros:")
        for i, nombre in enumerate(viajeros):
            print("Viajero {}: {}".format(i+1, nombre))
print("=====================================================\n")