import argparse
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def read_ids(ids_files):
    all_ids = []
    per_file = []

    for ids_file in ids_files:
        path = Path(ids_file)
        ids = [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        counts = Counter(ids)
        per_file.append(
            {
                "path": path,
                "rows": len(ids),
                "unique": len(counts),
                "duplicate_extra": sum(count - 1 for count in counts.values()),
                "duplicate_groups": sum(1 for count in counts.values() if count > 1),
            }
        )
        all_ids.extend(ids)

    return all_ids, per_file


def load_products(xml_file):
    root = ET.parse(xml_file).getroot()
    return root.findall("o")


def duplicate_summary(values):
    counts = Counter(values)
    duplicate_groups = {value: count for value, count in counts.items() if count > 1}
    return counts, duplicate_groups


def product_ean(product):
    for attr in product.findall("./attrs/a"):
        if attr.get("name") == "EAN":
            return (attr.text or "").strip()
    return ""


def sample_counter(counter, limit=20):
    return ", ".join(
        f"{value} x{count}" for value, count in sorted(counter.items())[:limit]
    )


def print_duplicate_examples(title, duplicate_groups, limit=20):
    if not duplicate_groups:
        return

    sample = Counter(duplicate_groups)
    print(f"{title}: {sample_counter(sample, limit)}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate whether filtered Ceneo XML matches oferta_medkon.xml "
            "filtered by selected ids*.txt files."
        )
    )
    parser.add_argument("ids_files", nargs="+", help="TXT files with product IDs")
    parser.add_argument(
        "--source",
        default="oferta_medkon.xml",
        help="Source XML file, default: oferta_medkon.xml",
    )
    parser.add_argument(
        "--output",
        default=f"oferta_filtered_{datetime.now().strftime('%d-%m-%Y')}.xml",
        help="Filtered XML file to validate, default: oferta_filtered_<today>.xml",
    )
    args = parser.parse_args()

    all_ids, per_file = read_ids(args.ids_files)
    allowed_ids = set(all_ids)
    all_id_counts, all_id_duplicates = duplicate_summary(all_ids)

    source_products = load_products(args.source)
    output_products = load_products(args.output)

    source_ids = [product.get("id") for product in source_products]
    output_ids = [product.get("id") for product in output_products]

    _, source_duplicate_ids = duplicate_summary(source_ids)
    output_id_counts, output_duplicate_ids = duplicate_summary(output_ids)

    expected_ids = [product_id for product_id in source_ids if product_id in allowed_ids]
    expected_counts = Counter(expected_ids)

    missing_from_source = allowed_ids - set(source_ids)
    unexpected_in_output = output_id_counts - expected_counts
    missing_from_output = expected_counts - output_id_counts
    order_matches = output_ids == expected_ids

    output_eans_by_value = defaultdict(list)
    for product in output_products:
        ean = product_ean(product)
        if ean:
            output_eans_by_value[ean].append(product.get("id"))
    duplicate_output_eans = {
        ean: ids for ean, ids in output_eans_by_value.items() if len(ids) > 1
    }

    print("=== FILTER XML VALIDATION ===")
    print(f"Source XML: {args.source}")
    print(f"Output XML: {args.output}")
    print(f"ID files: {', '.join(args.ids_files)}")
    print()
    print(f"ID rows loaded: {len(all_ids)}")
    print(f"Unique IDs loaded: {len(allowed_ids)}")
    print(f"Duplicate ID rows in selected TXT files: {len(all_ids) - len(allowed_ids)}")
    print(f"Duplicate ID groups in selected TXT files: {len(all_id_duplicates)}")
    print()

    for info in per_file:
        print(
            f"{info['path']}: rows={info['rows']}, unique={info['unique']}, "
            f"duplicate_rows={info['duplicate_extra']}, "
            f"duplicate_groups={info['duplicate_groups']}"
        )

    print()
    print(f"Products in source XML: {len(source_products)}")
    print(f"Unique product IDs in source XML: {len(set(source_ids))}")
    print(f"Duplicate product ID groups in source XML: {len(source_duplicate_ids)}")
    print(f"IDs from TXT not present in source XML: {len(missing_from_source)}")
    print(f"Expected products after filtering: {len(expected_ids)}")
    print(f"Products in output XML: {len(output_ids)}")
    print(f"Unique product IDs in output XML: {len(set(output_ids))}")
    print(f"Duplicate product ID groups in output XML: {len(output_duplicate_ids)}")
    print(f"Duplicate EAN groups in output XML: {len(duplicate_output_eans)}")
    print()

    if missing_from_source:
        print("Sample IDs from TXT missing in source XML:")
        print(", ".join(sorted(missing_from_source)[:20]))
        print()

    print_duplicate_examples("Sample duplicate IDs in selected TXT files", all_id_duplicates)
    print_duplicate_examples("Sample duplicate product IDs in source XML", source_duplicate_ids)
    print_duplicate_examples("Sample duplicate product IDs in output XML", output_duplicate_ids)

    if duplicate_output_eans:
        sample = sorted(duplicate_output_eans.items())[:20]
        print("Sample duplicate EANs in output XML:")
        for ean, ids in sample:
            print(f"{ean}: {', '.join(ids)}")
        print()

    ok = not unexpected_in_output and not missing_from_output and order_matches

    if unexpected_in_output:
        print("Unexpected product IDs in output XML:")
        print(sample_counter(unexpected_in_output))
        print()

    if missing_from_output:
        print("Expected product IDs missing from output XML:")
        print(sample_counter(missing_from_output))
        print()

    if not order_matches and not unexpected_in_output and not missing_from_output:
        print("Output has the right IDs, but product order differs from source XML.")
        print()

    if ok:
        print("PASS: output XML exactly matches source XML filtered by selected IDs.")
        return 0

    print("FAIL: output XML does not match source XML filtered by selected IDs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
