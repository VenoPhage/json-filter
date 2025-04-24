import json
import argparse


def filter_json(generated_file, filter_file, output_file):
    # Load the generated JSON data
    with open(generated_file, "r") as f:
        generated_data = json.load(f)

    # Load the filter JSON data
    with open(filter_file, "r") as f:
        filter_data = json.load(f)

    # Extract block values from the filter
    if isinstance(filter_data, list) and len(filter_data) > 0:
        if isinstance(filter_data[0], str):
            # Filter is a list of block strings
            filter_blocks = set(filter_data)
        else:
            # Filter is a list of objects with "block" keys
            filter_blocks = {item["block"] for item in filter_data}
    else:
        filter_blocks = set()

    # Filter the generated data
    filtered_data = [
        entry for entry in generated_data if entry.get("block") in filter_blocks
    ]

    # Save the filtered data to the output file
    with open(output_file, "w") as f:
        json.dump(filtered_data, f, indent=2)


def get_file_paths():
    parser = argparse.ArgumentParser(description="Filter JSON objects by block entries")
    parser.add_argument("--generated", help="Path to generated JSON file")
    parser.add_argument(
        "--filter", help="Path to filter JSON file", default="filter.json"
    )
    parser.add_argument(
        "--output", help="Path for output JSON file", default="filtered_data.json"
    )

    args = parser.parse_args()

    # Prompt for missing paths
    generated_file = args.generated or input("Enter path to generated JSON file: ")
    filter_file = args.filter or input("Enter path to filter JSON file: ")
    output_file = args.output or input("Enter path for output JSON file: ")

    return generated_file, filter_file, output_file


if __name__ == "__main__":
    generated_file, filter_file, output_file = get_file_paths()
    filter_json(generated_file, filter_file, output_file)
    print(f"Filtered data saved to {output_file}")
