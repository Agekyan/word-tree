"""
Main entry point for presidential speech word tree analysis.
"""

import os
import sys
from src.tokenizer import load_speeches, STOP_WORDS
from src.tree_builder import process_speeches_for_root
from src.exporter import export_split_json, print_tree_preview, generate_tree_statistics


def main():
    """
    Main execution pipeline for word tree analysis.
    """
    print("="*60)
    print("Presidential Speech Word Tree Analysis")
    print("="*60)
    print()

    # Configuration
    speeches_dir = '../speeches/'
    output_dir = '../visualization/data'
    root_words = ['we', 'must', 'freedom', 'fear', 'never']
    window_size = 5  # 4-5 words as specified

    # Step 1: Load all speeches
    print("Step 1: Loading speeches...")
    if not os.path.exists(speeches_dir):
        print(f"Error: Speeches directory '{speeches_dir}' not found.")
        sys.exit(1)

    speeches = load_speeches(speeches_dir)
    print(f"  Loaded {len(speeches)} speeches")
    print()

    if not speeches:
        print("Error: No speeches loaded. Exiting.")
        sys.exit(1)

    # Step 2: Process each root word
    print("Step 2: Processing root words...")
    results = {}

    for i, root in enumerate(root_words, 1):
        print(f"  [{i}/{len(root_words)}] Processing root word: '{root}'")

        # Build "after" tree
        print(f"      Building 'after' tree...")
        after_tree = process_speeches_for_root(speeches, root, direction='after',
                                              window_size=window_size,
                                              stop_words=STOP_WORDS)

        # Build "before" tree
        print(f"      Building 'before' tree...")
        before_tree = process_speeches_for_root(speeches, root, direction='before',
                                               window_size=window_size,
                                               stop_words=STOP_WORDS)

        # Store results
        results[root] = {
            'after': after_tree,
            'before': before_tree
        }

        # Print statistics
        after_stats = generate_tree_statistics(after_tree)
        before_stats = generate_tree_statistics(before_tree)

        print(f"      After tree: {after_stats['total_nodes']} nodes, "
              f"max depth {after_stats['max_depth']}")
        print(f"      Before tree: {before_stats['total_nodes']} nodes, "
              f"max depth {before_stats['max_depth']}")
        print()

    # Step 3: Export split JSON files
    print("Step 3: Exporting split JSON files...")
    export_split_json(results, speeches, output_dir)
    print()

    # Step 4: Print preview of first root word
    print("Step 4: Preview of first root word tree structure")
    print(f"Root word: '{root_words[0]}' (after direction)")
    print("-" * 60)
    print_tree_preview(results[root_words[0]]['after'], max_depth=3)
    print()

    print("="*60)
    print("Processing complete!")
    print(f"Output written to: {output_dir}/")
    print("="*60)


if __name__ == '__main__':
    main()
