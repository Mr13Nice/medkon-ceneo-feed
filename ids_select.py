import sys
from datetime import datetime
from pathlib import Path

from lxml import etree


INPUT_XML = "oferta_medkon.xml"
FIELDS = {
    "name": "name",
    "nazwa": "name",
    "producer": "producer",
    "producent": "producer",
}
PRODUCER_ATTR_NAMES = {"Producent", "Producent_*"}


def normalize_text(text):
    return " ".join((text or "").casefold().split())


def keyword_matches_text(keyword, text):
    return all(word in text for word in keyword.split())


def usage():
    print('Uzycie: python ids_select.py [name|producer] fraza1 "fraza z odstepem" ...')
    print('Przyklady:')
    print('  python ids_select.py avene "la roche"')
    print('  python ids_select.py name "avene spf"')
    print('  python ids_select.py producer boiron')


def parse_args(argv):
    if not argv:
        usage()
        sys.exit(1)

    first_arg = argv[0].casefold()
    if first_arg in FIELDS:
        field = FIELDS[first_arg]
        keywords = argv[1:]
    else:
        field = "name"
        keywords = argv

    if not keywords:
        usage()
        sys.exit(1)

    return field, [normalize_text(arg) for arg in keywords]


def offer_text_for_field(offer, field):
    if field == "name":
        name_elem = offer.find("name")
        return normalize_text(name_elem.text if name_elem is not None else "")

    producer_values = []
    for attr in offer.findall("./attrs/a"):
        if attr.get("name") in PRODUCER_ATTR_NAMES:
            producer_values.append(attr.text or "")

    return normalize_text(" ".join(producer_values))


def output_path(field, keywords):
    today = datetime.now().strftime("%d_%m_%Y")
    safe_keywords = [keyword.replace(" ", "_") for keyword in keywords]
    keywords_part = "_".join(safe_keywords)
    prefix = "ids" if field == "name" else f"ids_{field}"
    return Path(f"{prefix}_{keywords_part}_{today}.txt")


def main(argv):
    field, keywords = parse_args(argv)

    parser = etree.XMLParser(recover=True)
    tree = etree.parse(INPUT_XML, parser)
    root = tree.getroot()

    ids = []
    seen_ids = set()

    for offer in root.findall(".//o"):
        field_text = offer_text_for_field(offer, field)

        if any(keyword_matches_text(keyword, field_text) for keyword in keywords):
            product_id = offer.get("id")
            if product_id and product_id not in seen_ids:
                ids.append(product_id)
                seen_ids.add(product_id)

    path = output_path(field, keywords)
    with path.open("w", encoding="utf-8") as f:
        for product_id in ids:
            f.write(f"{product_id}\n")

    print(f"Zapisano {len(ids)} unikalnych ID do pliku {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
