import xml.etree.ElementTree as ET
import sys
from datetime import datetime

print("START SKRYPTU")
# sprawdzenie argumentow
if len(sys.argv) < 2:
    print("Podaj plik lub pliki z ID, np: python filter_xml.py ids_basic.txt ids_avene_sun.txt")
    sys.exit()

ids_files = sys.argv[1:]

# wczytanie list ID
allowed_ids = set()
total_ids = 0

for ids_file in ids_files:
    with open(ids_file, encoding="utf-8") as f:
        for line in f:
            product_id = line.strip()
            if product_id:
                total_ids += 1
                allowed_ids.add(product_id)

duplicates = total_ids - len(allowed_ids)

# wczytanie XML
tree = ET.parse("oferta_medkon.xml")
root = tree.getroot()

# filtrowanie
total_products = 0
kept_products = 0
found_ids = set()

for product in list(root.findall("o")):
    total_products += 1
    product_id = product.get("id")

    if product_id not in allowed_ids:
        root.remove(product)
    else:
        kept_products += 1
        found_ids.add(product_id)

missing_ids = allowed_ids - found_ids

#  generowanie daty
today = datetime.now().strftime("%d-%m-%Y")

# nazwa pliku
output_file = f"oferta_filtered_{today}.xml"

# zapis
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print("=== PODSUMOWANIE ===")
print(f"Pliki ID: {', '.join(ids_files)}")
print(f"Wczytanych ID: {total_ids}")
print(f"Unikalnych ID: {len(allowed_ids)}")
print(f"Usunietych duplikatow ID: {duplicates}")
print(f"Produktow w oferta_medkon.xml: {total_products}")
print(f"Produktow zapisanych do XML: {kept_products}")
print(f"ID nieobecnych w aktualnym XML: {len(missing_ids)}")

if missing_ids:
    sample_missing = ", ".join(sorted(missing_ids)[:20])
    print(f"Pierwsze brakujace ID: {sample_missing}")

print(f"Gotowe. Nowy plik: {output_file}")
