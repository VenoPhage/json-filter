import json
import argparse
import re


def filter_json(generated_file, filter_file, output_file, regex_pattern):
    with open(generated_file, "r") as f:
        generated_data = json.load(f)

    with open(filter_file, "r") as f:
        filter_data = json.load(f)

    modded_ore_pattern = re.compile(r"^(?!minecraft:)[^:]+:.+_ore$")

    if regex_pattern.strip() == "":
        modded_ore_pattern = None
        print("Regex filtering disabled")
    else:
        try:
            modded_ore_pattern = re.compile(regex_pattern)
            print(f"Using regex pattern: {regex_pattern}")
        except re.error as e:
            print(f"Invalid regex pattern: {e}")
            exit(1)

    filter_blocks = set(filter_data)
    filtered_data = [
        entry
        for entry in generated_data
        if (
            entry.get("block") in filter_blocks
            or (modded_ore_pattern and modded_ore_pattern.match(entry.get("block", "")))
        )
    ]

    matched_blocks = sorted({entry.get("block") for entry in filtered_data})

    print("\nMatched blocks:")
    for block in matched_blocks:
        print(f" - {block}")

    response = input("\nIs this list correct? (y/n): ").strip().lower()
    if response != "y":
        print("Aborting - no changes saved.")
        exit()

    with open(output_file, "w") as f:
        json.dump(filtered_data, f, indent=2)


def get_file_paths():
    default_regex = r"^(?!minecraft:)[^:]+:.+_ore$"

    parser = argparse.ArgumentParser(description="Filter JSON objects by block entries")
    parser.add_argument("--generated", help="Path to generated JSON file")
    parser.add_argument(
        "--filter", help="Path to filter JSON file", default="filter.json"
    )
    parser.add_argument(
        "--output", help="Path for output JSON file", default="world-gen.json"
    )
    parser.add_argument(
        "--regex",
        help=f"Custom regex pattern for modded ores. Default: '{default_regex}'",
        default=default_regex,
    )

    args = parser.parse_args()

    generated_file = args.generated or input("Enter path to generated JSON file: ")
    filter_file = args.filter or input("Enter path to filter JSON file: ")
    output_file = args.output or input("Enter path for output JSON file: ")

    return generated_file, filter_file, output_file, args.regex


if __name__ == "__main__":
    generated_file, filter_file, output_file, regex_pattern = get_file_paths()
    filter_json(generated_file, filter_file, output_file, regex_pattern)
    print(f"\nFiltered data saved to {output_file}")
