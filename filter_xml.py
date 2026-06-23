import xml.etree.ElementTree as ET
import sys
from datetime import datetime
from pathlib import Path


CONFIG_FILE = Path("offer_sources.txt")
INPUT_XML = Path("oferta_medkon.xml")


def read_config(config_file):
    if not config_file.is_file():
        raise FileNotFoundError(
            f"Nie znaleziono pliku konfiguracyjnego {config_file}. "
            "Podaj pliki ID w komendzie albo utworz offer_sources.txt."
        )

    ids_files = []
    for line in config_file.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            ids_files.append(value)

    if not ids_files:
        raise ValueError(f"Plik {config_file} nie zawiera zadnych plikow ID.")

    return ids_files


def resolve_ids_files(arguments):
    if arguments:
        return arguments, "argumenty komendy"
    return read_config(CONFIG_FILE), str(CONFIG_FILE)


def validate_input_files(ids_files):
    missing_files = [path for path in ids_files if not Path(path).is_file()]
    if missing_files:
        missing_list = ", ".join(missing_files)
        raise FileNotFoundError(f"Nie znaleziono plikow ID: {missing_list}")

    if not INPUT_XML.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku {INPUT_XML}.")


def main(arguments):
    print("START SKRYPTU")

    try:
        ids_files, source = resolve_ids_files(arguments)
        validate_input_files(ids_files)
    except (FileNotFoundError, ValueError) as error:
        print(f"BLAD: {error}")
        return 1

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
    tree = ET.parse(INPUT_XML)
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

    today = datetime.now().strftime("%d-%m-%Y")
    output_file = f"oferta_filtered_{today}.xml"
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    print("=== PODSUMOWANIE ===")
    print(f"Zrodlo listy plikow: {source}")
    print(f"Pliki ID: {', '.join(ids_files)}")
    print(f"Wczytanych ID: {total_ids}")
    print(f"Unikalnych ID: {len(allowed_ids)}")
    print(f"Usunietych duplikatow ID: {duplicates}")
    print(f"Produktow w {INPUT_XML}: {total_products}")
    print(f"Produktow zapisanych do XML: {kept_products}")
    print(f"ID nieobecnych w aktualnym XML: {len(missing_ids)}")

    if missing_ids:
        sample_missing = ", ".join(sorted(missing_ids)[:20])
        print(f"Pierwsze brakujace ID: {sample_missing}")

    print(f"Gotowe. Nowy plik: {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
