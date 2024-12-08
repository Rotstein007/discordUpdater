#!/usr/bin/env python3
# Dieses Skript aktualisiert die build_info.json Datei von Discord oder Discord Canary.
# Autor: Rotstein
# Lizenz: MIT

import json
import os
import requests

def hole_aktuellste_version(kanal):
    """Ermittelt die neueste Version von Discord oder Discord Canary."""
    url = f"https://discord.com/api/updates/{kanal}"
    try:
        antwort = requests.get(url)
        antwort.raise_for_status()
        daten = antwort.json()

        # Extrahiere die Version aus der JSON-Antwort
        version = daten.get("name", "")  # Feld "name" enthält die Versionsnummer
        if version:
            return version
        else:
            raise ValueError("Konnte die Version nicht aus der API-Antwort extrahieren.")
    except Exception as e:
        print(f"Fehler beim Abrufen der neuesten Version für {kanal}: {e}")
        exit(1)

def lese_aktuelle_version(dateipfad):
    """Liest die aktuelle Version aus der build_info.json Datei."""
    try:
        with open(dateipfad, "r") as f:
            daten = json.load(f)
        return daten.get("version", "")
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {dateipfad}. Es wird angenommen, dass keine aktuelle Version vorhanden ist.")
        return ""
    except json.JSONDecodeError:
        print(f"Fehler beim Lesen der JSON-Daten aus {dateipfad}. Bitte die Datei überprüfen.")
        exit(1)

def aktualisiere_build_info(dateipfad, kanal, version):
    """Aktualisiert die build_info.json Datei mit der neuen Version."""
    build_info = {
        "releaseChannel": kanal,
        "version": version
    }
    try:
        ausgabe = json.dumps(build_info, indent=4)
        os.system(f"echo '{ausgabe}' | sudo /usr/bin/tee {dateipfad} > /dev/null")
        print(f"Auf Version {version} aktualisiert.")
    except Exception as e:
        print(f"Fehler beim Aktualisieren der build_info.json für {kanal}: {e}")
        exit(1)

def finde_installed_discords():
    """Prüft, welche Discord-Versionen installiert sind, und gibt die relevanten Konfigurationen zurück."""
    konfigurationen = []
    if os.path.exists("/opt/discord/resources/build_info.json"):
        konfigurationen.append(("stable", "/opt/discord/resources/build_info.json"))
    if os.path.exists("/opt/discord-canary/resources/build_info.json"):
        konfigurationen.append(("canary", "/opt/discord-canary/resources/build_info.json"))

    if not konfigurationen:
        print("Keine Discord-Installation gefunden. Bitte installieren Sie Discord oder Discord Canary.")
        exit(1)

    return konfigurationen

def hauptprogramm():
    # Automatische Erkennung der installierten Discord-Versionen
    konfigurationen = finde_installed_discords()

    for kanal, build_info_pfad in konfigurationen:
        neueste_version = hole_aktuellste_version(kanal)
        aktuelle_version = lese_aktuelle_version(build_info_pfad)

        # Benutzerfreundliche Ausgabe
        if aktuelle_version == neueste_version:
            print(f"{kanal.capitalize()}:")
            print(f"Aktuelle Version: {aktuelle_version}")
            print(f"Neue Version: {neueste_version}")
            print("Keine neue Version verfügbar.")
        else:
            print(f"{kanal.capitalize()}:")
            print(f"Aktuelle Version: {aktuelle_version}")
            print(f"Neue Version: {neueste_version}")
            aktualisiere_build_info(build_info_pfad, kanal, neueste_version)

if __name__ == "__main__":
    hauptprogramm()
