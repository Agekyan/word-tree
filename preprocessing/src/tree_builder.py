"""
Word tree building functionality for creating hierarchical structures.
"""

from typing import List, Dict, Tuple
from collections import defaultdict
from .tokenizer import normalize_word


def find_root_occurrences(tokens: List[str], root: str) -> List[int]:
    """
    Find all positions where the root word appears (case-insensitive).

    Args:
        tokens: List of word tokens from speech
        root: Root word to search for (will be normalized)

    Returns:
        List of indices where root word appears
    """
    root_normalized = root.lower()
    positions = []

    for i, token in enumerate(tokens):
        if normalize_word(token) == root_normalized:
            positions.append(i)

    return positions


def extract_context_window(tokens: List[str], root_position: int,
                           direction: str, window_size: int = 5) -> List[str]:
    """
    Extract N words before or after the root word position.

    Args:
        tokens: List of word tokens from speech
        root_position: Index of root word in tokens
        direction: Either "after" or "before"
        window_size: Number of words to extract (default 5)

    Returns:
        List of words in the context window (may be shorter than window_size
        if near beginning/end of speech)
    """
    if direction == "after":
        start = root_position + 1
        end = min(start + window_size, len(tokens))
        return tokens[start:end]

    elif direction == "before":
        end = root_position
        start = max(0, end - window_size)
        # Reverse the order so it reads backward from root
        return tokens[start:end][::-1]

    else:
        raise ValueError(f"Invalid direction: {direction}. Must be 'after' or 'before'.")


def build_tree(occurrences: List[Tuple[List[str], Dict]], root: str) -> Dict:
    """
    Build hierarchical tree structure from all occurrences.

    Args:
        occurrences: List of tuples (context_words, speech_metadata)
        root: Root word name

    Returns:
        Tree structure as nested dictionary
    """
    # Recursive function to build tree from sequences
    def add_sequence_to_tree(tree_node: Dict, sequence: List[str],
                            metadata: Dict, depth: int = 0):
        """
        Recursively add a word sequence to the tree.

        Args:
            tree_node: Current node in the tree
            sequence: Remaining words in the sequence
            metadata: Speech metadata to attach
            depth: Current depth in tree
        """
        if not sequence:
            return

        # Normalize first word in sequence for matching
        word = sequence[0]
        word_normalized = normalize_word(word)

        # Initialize children dict if not exists
        if 'children' not in tree_node:
            tree_node['children'] = {}

        # Get or create child node for this word
        if word_normalized not in tree_node['children']:
            tree_node['children'][word_normalized] = {
                'name': word_normalized,
                'value': 0,
                'metadata': {
                    'eras': defaultdict(int),
                    'speakers': defaultdict(int),
                }
            }

        child = tree_node['children'][word_normalized]

        # Increment count
        child['value'] += 1

        # Add metadata
        child['metadata']['eras'][metadata['era']] += 1
        child['metadata']['speakers'][metadata['president']] += 1

        # Recursively process remaining words
        if len(sequence) > 1:
            add_sequence_to_tree(child, sequence[1:], metadata, depth + 1)

    # Initialize root node
    tree = {
        'name': root,
        'children': {}
    }

    # Add all occurrences to tree
    for context_words, metadata in occurrences:
        add_sequence_to_tree(tree, context_words, metadata)

    return tree


def convert_tree_to_list(tree_node: Dict) -> Dict:
    """
    Convert tree structure from dict of children to list of children.

    This is the final format expected by D3.js.

    Args:
        tree_node: Tree node with children as dict

    Returns:
        Tree node with children as list
    """
    if 'children' not in tree_node or not tree_node['children']:
        return tree_node

    # Convert children dict to list
    children_list = []
    for child_name, child_node in tree_node['children'].items():
        # Recursively convert child nodes
        converted_child = convert_tree_to_list(child_node)

        # Convert defaultdicts to regular dicts for JSON serialization
        if 'metadata' in converted_child:
            converted_child['metadata']['eras'] = dict(converted_child['metadata']['eras'])
            converted_child['metadata']['speakers'] = dict(converted_child['metadata']['speakers'])

        children_list.append(converted_child)

    # Sort children by value (count) in descending order
    children_list.sort(key=lambda x: x.get('value', 0), reverse=True)

    tree_node['children'] = children_list

    return tree_node


def process_speeches_for_root(speeches: List[Dict], root: str,
                              direction: str, window_size: int = 5,
                              stop_words=None) -> Dict:
    """
    Process all speeches to build tree for a specific root word and direction.

    Args:
        speeches: List of speech dictionaries
        root: Root word to analyze
        direction: Either "after" or "before"
        window_size: Context window size (default 5)

    Returns:
        Complete tree structure for this root word
    """
    from .tokenizer import clean_text, tokenize_speech
    from .metadata import parse_date, assign_era

    occurrences = []

    for speech in speeches:
        # Get and clean transcript
        transcript = speech.get('transcript', '')
        if not transcript:
            continue

        clean_transcript = clean_text(transcript)
        tokens = tokenize_speech(clean_transcript)

        # Find root occurrences
        root_positions = find_root_occurrences(tokens, root)

        # Extract context for each occurrence
        for pos in root_positions:
            context_words = extract_context_window(tokens, pos, direction, window_size)

            if stop_words:
                from .tokenizer import filter_stop_words
                context_words = filter_stop_words(context_words, stop_words)

            if not context_words:
                continue

            # Prepare metadata
            date = parse_date(speech['date'])
            era = assign_era(date)

            metadata = {
                'president': speech['president'],
                'date': speech['date'],
                'era': era,
                'title': speech['title'],
            }

            occurrences.append((context_words, metadata))

    # Build tree from all occurrences
    tree = build_tree(occurrences, root)

    # Convert to list format for D3.js
    tree = convert_tree_to_list(tree)

    return tree
