*** MEDKON - skrócona instrukcja ***

Komendy uruchamiaj w PowerShell w folderze projektu.

1. Zaktualizuj "oferta_medkon.xml" (ta sama operacja co automatyczne zadanie codziennie o 9:30):
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\update_oferta_medkon.ps1 -KeepBackup

Skrypt pobiera i sprawdza ofertę. Poprzednia wersja: "oferta_medkon.xml.bak".
Log aktualizacji: "oferta_medkon_update.log".

2. W pliku "offer_sources.txt" wpisz nazwy list ID produktów, po jednej w wierszu.

3. Wygeneruj przefiltrowany XML dla Ceneo:
python filter_xml.py

4. Uruchom aktualizację ofert InPost po zmianie CSV:
npm run inpost:update-after-csv

Komenda przekazuje wykonanie do projektu ..\..\Suppla\suppla-api. Dane CSV,
konfiguracja .env, zależności i właściwa logika InPost pozostają w tamtym
projekcie. Przed uruchomieniem włącz tam serwer InPost poleceniem
node server.js w osobnym terminalu.

Pełna instrukcja: README.txt.
