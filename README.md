# json filter
Intended for use with [Region Scanner](https://github.com/RundownRhino/RegionScanner)

## Usage
1. Generate a JSON file using [Region Scanner](https://github.com/RundownRhino/RegionScanner)
2. Run `python main.py --generated <path/to/generated/json/file>`

## Arguments
- `--generated`: Path to generated JSON file
- `--filter`: Path to filter JSON file (default: `filter.json`)
- `--output`: Path for output JSON file (default: `filtered_data.json`)
- `--regex`: Custom regex pattern for modded ores