import csv
import json
import os
import xml.etree.ElementTree as ET

import requests


url = "https://sandboxdnac.cisco.com"
user = os.getenv("CATALYST_USER", "devnetuser")
password = os.getenv("CATALYST_PASSWORD")

if not password:
    raise SystemExit("Falta la variable CATALYST_PASSWORD.")

try:
    respuesta = requests.post(
        url + "/dna/system/api/v1/auth/token",
        auth=(user, password),
        verify=False,
        timeout=20,
    )
    respuesta.raise_for_status()
    token = respuesta.json()["Token"]

    respuesta = requests.get(
        url + "/dna/intent/api/v1/network-device",
        headers={"X-Auth-Token": token},
        verify=False,
        timeout=30,
    )
    respuesta.raise_for_status()
    dispositivos = respuesta.json()["response"]

    filas = []
    for d in dispositivos:
        fila = {
            "id": d.get("id", ""),
            "nombre": d.get("hostname", ""),
            "ip": d.get("managementIpAddress", ""),
            "tipo": d.get("family", ""),
            "estado": d.get("reachabilityStatus", ""),
            "version": d.get("softwareVersion", ""),
        }
        if not fila["id"] or not fila["nombre"] or not fila["ip"]:
            raise ValueError("La API devolvió un dispositivo incompleto.")
        filas.append(fila)

    if not filas:
        raise ValueError("La API no devolvió dispositivos.")

    os.makedirs("reports", exist_ok=True)

    with open("reports/inventory.json", "w") as archivo:
        json.dump(filas, archivo, indent=2)

    with open("reports/inventory.csv", "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=filas[0].keys())
        escritor.writeheader()
        escritor.writerows(filas)

    raiz = ET.Element("dispositivos")
    for fila in filas:
        dispositivo = ET.SubElement(raiz, "dispositivo")
        for campo, valor in fila.items():
            ET.SubElement(dispositivo, campo).text = valor

    ET.ElementTree(raiz).write(
        "reports/inventory.xml",
        encoding="utf-8",
        xml_declaration=True,
    )

    print("Dispositivos consultados:", len(filas))
    print("Reportes guardados en la carpeta reports.")

except requests.HTTPError as error:
    print("Error HTTP:", error.response.status_code)
except requests.RequestException as error:
    print("Error de conexión:", error)
except (KeyError, ValueError) as error:
    print("Error en los datos:", error)