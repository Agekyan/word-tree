"""
Speech loading and tokenization functionality.
"""

import json
import os
import re
from typing import List, Dict, Set


STOP_WORDS = {
    'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'yet', 'so',
    'in', 'on', 'at', 'to', 'by', 'of', 'up', 'as', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
    'might', 'shall', 'can', 'this', 'that', 'these', 'those',
    'it', 'its', 'with', 'from', 'into', 'through', 'not', 'no',
    'i', 'my', 'me', 'he', 'she', 'they', 'their', 'our', 'your',
    'his', 'her', 'we', 'you', 'us', 'them', 'who', 'which', 'what',
    'all', 'each', 'more', 'than', 'when', 'if', 'then', 'there',
}


def load_speeches(speeches_dir: str) -> List[Dict]:
    """
    Load all speech JSON files from the specified directory.

    Args:
        speeches_dir: Path to directory containing speech JSON files

    Returns:
        List of speech dictionaries with metadata
    """
    speeches = []

    for filename in os.listdir(speeches_dir):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(speeches_dir, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                speech_data = json.load(f)

                # Extract relevant fields
                speech = {
                    'title': speech_data.get('title', ''),
                    'president': speech_data.get('president', ''),
                    'date': speech_data.get('date', ''),
                    'transcript': speech_data.get('transcript', ''),
                    'url': speech_data.get('url', ''),
                }

                speeches.append(speech)

        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading {filename}: {e}")
            continue

    return speeches


def clean_text(text: str) -> str:
    """
    Remove HTML tags and normalize whitespace in text.

    Args:
        text: Raw transcript text potentially containing HTML

    Returns:
        Cleaned text string
    """
    # Remove HTML tags like <br />, <p>, etc.
    text = re.sub(r'<[^>]+>', ' ', text)

    # Remove \r\n escape sequences
    text = text.replace('\\r\\n', ' ')
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')

    # Normalize multiple spaces to single space
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def tokenize_speech(text: str) -> List[str]:
    """
    Split text into word tokens.

    Splits on whitespace while keeping punctuation attached to words.
    This preserves the natural structure for context extraction.

    Args:
        text: Cleaned text string

    Returns:
        List of word tokens
    """
    # Split on whitespace
    tokens = text.split()

    return tokens


def strip_punctuation(word: str) -> str:
    """
    Remove leading and trailing punctuation from a word.

    Used for case-insensitive matching while preserving the original
    word with punctuation for display purposes.

    Args:
        word: Word token potentially with punctuation

    Returns:
        Word without leading/trailing punctuation
    """
    # Strip common punctuation from start and end
    word = word.strip('.,;:!?"\'-()[]{}')

    return word


def normalize_word(word: str) -> str:
    """
    Normalize word for case-insensitive matching.

    Args:
        word: Original word token

    Returns:
        Lowercase word without punctuation
    """
    word = strip_punctuation(word)
    word = word.lower()

    return word


def filter_stop_words(words: List[str], stop_words: Set[str]) -> List[str]:
    """
    Truncate a word sequence at the first stop word.

    Truncation preserves strict adjacency between tree nodes — removing stop
    words from the middle of a sequence would create false connections between
    words that were not actually neighbors.

    Args:
        words: List of tokens (may contain punctuation)
        stop_words: Set of normalized stop words to truncate at

    Returns:
        Prefix of words up to (not including) the first stop word
    """
    for i, word in enumerate(words):
        if normalize_word(word) in stop_words:
            return words[:i]
    return words
