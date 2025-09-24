#!/usr/bin/env python3
"""
Script to generate a normalized roles-to-names mapping from JSON data.

This script reads a JSON file containing role and profile information,
then creates a mapping where each role maps to a sorted, deduplicated,
and trimmed list of profile names.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def normalize_roles_to_names(input_data):
    """
    Convert input data to normalized roles-to-names mapping.
    
    Args:
        input_data (list): List of dictionaries with 'RECHT' and 'PROFIEL' keys
        
    Returns:
        dict: Mapping of roles to sorted, deduplicated, trimmed profile names
    """
    roles_mapping = defaultdict(set)
    
    for item in input_data:
        role = item.get('RECHT')
        profile = item.get('PROFIEL')
        
        if role and profile:
            # Trim whitespace and add to the set for deduplication
            roles_mapping[role].add(profile.strip())
    
    # Convert sets to sorted lists
    normalized_mapping = {}
    for role, profiles in roles_mapping.items():
        normalized_mapping[role] = sorted(list(profiles))
    
    return normalized_mapping


def process_json_file(input_file_path, output_file_path):
    """
    Process a JSON file and create the normalized roles-to-names mapping.
    
    Args:
        input_file_path (str or Path): Path to input JSON file
        output_file_path (str or Path): Path to output JSON file
    """
    input_path = Path(input_file_path)
    output_path = Path(output_file_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read input JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # Generate normalized mapping
    roles_to_names = normalize_roles_to_names(input_data)
    
    # Write output JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(roles_to_names, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully created roles-to-names mapping: {output_path}")
    print(f"Found {len(roles_to_names)} unique roles:")
    for role, names in roles_to_names.items():
        print(f"  {role}: {len(names)} unique profile(s)")


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 3:
        print("Usage: python pivot_roles.py <input_json_file> <output_json_file>")
        print("Example: python pivot_roles.py Result_28.json data/roles-to-names.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        process_json_file(input_file, output_file)
    except Exception as e:
        print(f"Error processing files: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()