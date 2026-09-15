*** MEDKON - skrócona instrukcja ***

Komendy uruchamiaj w PowerShell w folderze projektu.

1. Zaktualizuj "oferta_medkon.xml" (ta sama operacja co automatyczne zadanie codziennie o 9:30):
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\update_oferta_medkon.ps1 -KeepBackup

Skrypt pobiera i sprawdza ofertę. Poprzednia wersja: "oferta_medkon.xml.bak".
Log aktualizacji: "oferta_medkon_update.log".

2. W pliku "offer_sources.txt" wpisz nazwy list ID produktów, po jednej w wierszu.

3. Wygeneruj przefiltrowany XML dla Ceneo:
python filter_xml.py

Pełna instrukcja: README.txt.
