import sys
from lxml import etree
from datetime import datetime

def normalize_text(text):
    return " ".join(text.casefold().split())

# sprawdzenie argumentów
if len(sys.argv) < 2:
    print('Użycie: python ids_select.py fraza1 "fraza z odstępem" ...')
    sys.exit(1)

# słowa kluczowe
KEYWORDS = [normalize_text(arg) for arg in sys.argv[1:]]

INPUT_XML = "oferta_medkon.xml"

# przygotowanie nazwy pliku (frazy + data)
today = datetime.now().strftime("%d_%m_%Y")

# usunięcie ewentualnych dziwnych znaków z fraz
safe_keywords = [k.replace(" ", "_") for k in KEYWORDS]
keywords_part = "_".join(safe_keywords)

OUTPUT_TXT = f"ids_{keywords_part}_{today}.txt"

parser = etree.XMLParser(recover=True)
tree = etree.parse(INPUT_XML, parser)
root = tree.getroot()

ids = []
seen_ids = set()

for offer in root.findall(".//o"):
    name_elem = offer.find("name")
    
    if name_elem is not None and name_elem.text:
        name_text = normalize_text(name_elem.text)
        
        if any(keyword in name_text for keyword in KEYWORDS):
            product_id = offer.get("id")
            if product_id and product_id not in seen_ids:
                ids.append(product_id)
                seen_ids.add(product_id)

# zapis do pliku
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    for _id in ids:
        f.write(f"{_id}\n")

print(f"Zapisano {len(ids)} unikalnych ID do pliku {OUTPUT_TXT}")
