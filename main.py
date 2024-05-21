import requests
import zipfile
import os
import io
import shutil
import tkinter as tk
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from SteamPathFinder import get_game_path,get_steam_path

colorama_init()

downloadDir = "./virus_vorsicht/"
BEPINEX = "https://thunderstore.io/package/download/BepInEx/BepInExPack/5.4.2100/"

#Lethal Company
MORE_COMPANY = "https://thunderstore.io/package/download/notnotnotswipez/MoreCompany/1.9.1/"
MORE_SUITS = "https://thunderstore.io/package/download/x753/More_Suits/1.4.3/"
MORE_EMOTES = "https://thunderstore.io/package/download/Sligili/More_Emotes/1.3.3/" #"https://thunderstore.io/package/download/Sligili/More_Emotes/1.2.2/" #Neuere Versionen funktionierten nicht
OZONE_RUNTIME = "https://thunderstore.io/package/download/Ozone/Runtime_Netcode_Patcher/0.2.5/"

#Content Warning
VIRALITY = "https://thunderstore.io/package/download/MaxWasUnavailable/Virality/1.4.0/"

vorbidden_list = []
# currentPath = os.path.abspath(os.curdir)
steam_path = get_steam_path()
try:
    lethal_company = get_game_path(steam_path,"1966720","Lethal Company")
    print(f"{Fore.GREEN}{lethal_company}{Style.RESET_ALL}")
    lethal_company_Plugins = lethal_company + "\\BepInEx\\plugins"
except:
    vorbidden_list.append(1)
try:
    content_warning = get_game_path(steam_path,"2881650","Content Warning")
    print(f"{Fore.GREEN}{content_warning}{Style.RESET_ALL}")
    content_warning_Plugins = content_warning + "\\BepInEx\\plugins"
except:
    vorbidden_list.append(2)

def move_and_replace(src, dest):
    # print("Quelle: ",src)
    # print("Ziel: ",dest)
    # Iteriere durch alle Dateien und Unterverzeichnisse im Quellverzeichnis
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        
        # Falls der Quellpfad ein Verzeichnis ist
        if os.path.isdir(s):
            # Erstelle das Verzeichnis im Zielpfad, falls es nicht existiert
            if not os.path.exists(d):
                os.makedirs(d)
            # Rekursive Verschiebung der Inhalte des Verzeichnisses
            move_and_replace(s, d)
        else:
            # Wenn es eine Datei ist, verschiebe sie und ersetze existierende Dateien
            if os.path.exists(d):
                os.remove(d)
            shutil.move(s, d)

def remove_dir(path):
    if not os.path.isdir(path):
        return
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        for file in filenames:
            os.remove(os.path.join(dirpath, file))
        for dir in dirnames:
            shutil.rmtree(os.path.join(dirpath, dir))
    shutil.rmtree(path)

def install_lethal():

    downLoadUrls = [
        BEPINEX,
        MORE_EMOTES,
        MORE_SUITS,
        MORE_COMPANY,
        OZONE_RUNTIME
        ]
    number = 0

    for i in downLoadUrls:
        number += 1
        response = requests.get(i)
        if checkResponse(response):
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(f"{downloadDir}{number}")
            print(f"{Fore.GREEN} Datei gespeichert{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Fehler beim Herrunterladen{Style.RESET_ALL}")

    move_and_replace(f"{downloadDir}1/BepInExPack",lethal_company)
    if(not(os.path.exists(lethal_company_Plugins))):
        _ = input(f"{Fore.RED}Starte Lethal Company. Nach dem Das Spiel wieder beendet wurde Enter drücken.{Style.RESET_ALL}")
    move_and_replace(f"{downloadDir}2/BepInEx/plugins",lethal_company_Plugins)
    move_and_replace(f"{downloadDir}3/BepInEx/plugins",lethal_company_Plugins)
    move_and_replace(f"{downloadDir}4/BepInEx/plugins",lethal_company_Plugins)
    #move_and_replace(f"{downloadDir}5/NicholaScott.BepInEx.RuntimeNetcodeRPCValidator.dll",lethal_company_Plugins)
    shutil.move(f"{downloadDir}5/NicholaScott.BepInEx.RuntimeNetcodeRPCValidator.dll", lethal_company_Plugins+"/NicholaScott.BepInEx.RuntimeNetcodeRPCValidator.dll")
    remove_dir(f"{downloadDir}")

def install_Content_warning():
    downLoadUrls = [
        BEPINEX,
        VIRALITY
        ]
    number = 0

    for i in downLoadUrls:
        number += 1
        response = requests.get(i)
        if checkResponse(response):
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(f"{downloadDir}{number}")
            print(f"{Fore.GREEN} Datei gespeichert{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Fehler beim Herrunterladen{Style.RESET_ALL}")

    
    move_and_replace(f"{downloadDir}1/BepInExPack",content_warning)
    if(not(os.path.exists(content_warning_Plugins))):
        _ = input(f"{Fore.RED}Starte Content Warning. Nach dem Das Spiel wieder beendet wurde Enter drücken.{Style.RESET_ALL}")
    move_and_replace(f"{downloadDir}2/BepInEx/plugins",content_warning_Plugins)
    # move_and_replace(f"{downloadDir}3/BepInEx/plugins",content_warning_Plugins)
    # move_and_replace(f"{downloadDir}4/BepInEx/plugins",content_warning_Plugins)
    remove_dir(f"{downloadDir}")

def checkResponse(code):
    if code.status_code == 200:
        return True

def main():
    auswahl = 0
    try:
        auswahl = int(input("Für welches Game sollen die Mods installiert werden?\n(1) Lethal Company\n(2) Content Warning\n Nur die Vorranstehende Zahl eingeben.\n"))
    except:
        pass
    while auswahl in vorbidden_list or auswahl < 1 or auswahl > 2:
        try:
            auswahl = int(input("Falsche Eingabe. \n(1) Lethal Company\n(2) Content Warning\nNur die Vorranstehende Zahl eingeben.\n"))
        except:
            pass
    
    match auswahl:
        case 1:
            return install_lethal()
        case 2:
            return install_Content_warning()


if __name__ == "__main__":
    main()