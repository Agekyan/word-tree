"""
JSON export functionality for D3.js visualization.
"""

import json
import os
from typing import Dict, List
from datetime import datetime


def export_split_json(root_word_trees: Dict, speeches: List[Dict],
                      output_dir: str) -> None:
    """
    Export word tree data as split JSON files for on-demand loading.

    Writes:
      {output_dir}/metadata.json        - global metadata
      {output_dir}/{root_word}.json     - per-root-word tree data

    Args:
        root_word_trees: Dictionary mapping root words to their tree structures
                        Format: {root_word: {'after': tree, 'before': tree}}
        speeches: List of all speeches (for metadata generation)
        output_dir: Directory to write all output files into
    """
    from .metadata import get_all_eras, parse_date

    os.makedirs(output_dir, exist_ok=True)

    # Collect global metadata
    presidents = sorted(set(speech['president'] for speech in speeches))
    eras = get_all_eras()

    # Find date range
    dates = [parse_date(speech['date']) for speech in speeches if speech.get('date')]
    if dates:
        min_date = min(dates)
        max_date = max(dates)
        date_range = [min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')]
    else:
        date_range = []

    # Write metadata.json
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_speeches': len(speeches),
                'date_range': date_range,
                'eras': eras,
                'presidents': presidents,
                'root_words_analyzed': list(root_word_trees.keys()),
            }
        }, f, indent=2, ensure_ascii=False)
    size_kb = os.path.getsize(metadata_path) / 1024
    print(f"  Created {metadata_path} ({size_kb:.2f} KB)")

    # Write one file per root word
    for root_word, tree_data in root_word_trees.items():
        word_path = os.path.join(output_dir, f'{root_word}.json')
        with open(word_path, 'w', encoding='utf-8') as f:
            json.dump(tree_data, f, indent=2, ensure_ascii=False)
        size_mb = os.path.getsize(word_path) / (1024 * 1024)
        print(f"  Created {word_path} ({size_mb:.2f} MB)")

    print(f"Total speeches processed: {len(speeches)}")
    print(f"Root words analyzed: {', '.join(root_word_trees.keys())}")
    print(f"Date range: {date_range[0] if date_range else 'N/A'} to {date_range[1] if date_range else 'N/A'}")


def generate_tree_statistics(tree: Dict) -> Dict:
    """
    Generate statistics about a tree structure.

    Args:
        tree: Tree structure

    Returns:
        Dictionary of statistics
    """
    def count_nodes(node: Dict) -> int:
        """Recursively count nodes in tree."""
        count = 1
        if 'children' in node and node['children']:
            for child in node['children']:
                count += count_nodes(child)
        return count

    def max_depth(node: Dict, current_depth: int = 0) -> int:
        """Find maximum depth of tree."""
        if 'children' not in node or not node['children']:
            return current_depth

        return max(max_depth(child, current_depth + 1) for child in node['children'])

    stats = {
        'total_nodes': count_nodes(tree),
        'max_depth': max_depth(tree),
        'root_name': tree.get('name', 'unknown'),
    }

    return stats


def print_tree_preview(tree: Dict, max_depth: int = 3, indent: int = 0) -> None:
    """
    Print a preview of the tree structure for debugging.

    Args:
        tree: Tree structure
        max_depth: Maximum depth to print
        indent: Current indentation level
    """
    name = tree.get('name', 'unknown')
    value = tree.get('value', 0)

    print('  ' * indent + f"{name} ({value})")

    if indent < max_depth and 'children' in tree and tree['children']:
        # Print top 5 children only
        for child in tree['children'][:5]:
            print_tree_preview(child, max_depth, indent + 1)

        if len(tree['children']) > 5:
            print('  ' * (indent + 1) + f"... and {len(tree['children']) - 5} more")
