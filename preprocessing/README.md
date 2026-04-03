# Data Preprocessor

## Dependencies

- Python 3.8 or higher
- Standard library only (no external packages required)

## Usage

### Running the Analysis

```bash
python3 main.py
```

This will:
1. Load all 1,056 speeches from `speeches/` directory
2. Process each root word (we, must, freedom, fear, never)
3. Build word trees for both "after" and "before" directions
4. Export results to `output/word_tree_data.json`

### Output Format

The output JSON has the following structure:

```json
{
  "root_words": {
    "freedom": {
      "after": {
        "name": "freedom",
        "children": [
          {
            "name": "and",
            "value": 429,
            "metadata": {
              "eras": {
                "Cold War": 150,
                "Modern Era": 120,
                ...
              },
              "speakers": {
                "Ronald Reagan": 45,
                "Barack Obama": 38,
                ...
              }
            },
            "children": [...]
          }
        ]
      },
      "before": { ... }
    }
  },
  "metadata": {
    "total_speeches": 1056,
    "date_range": ["1789-04-30", "2026-02-28"],
    "eras": [...],
    "presidents": [...]
  }
}
```

### Node Structure

Each tree node contains:
- `name`: The word at this position
- `value`: Number of occurrences (for node sizing in D3.js)
- `metadata`: Era and speaker distributions (for color coding)
- `children`: Array of child nodes (words that follow)

## Example Word Sequences

From the "we" root word analysis:

**After "we":**
- we → have → to → do
- we → are → not → going → to
- we → will → not → be
- we → must → be → prepared
- we → can → do → it

**Before "we":**
- [words] → [words] → [words] → [words] → we

## Implementation Details

### Tokenization
- Simple whitespace splitting
- Punctuation preserved initially, stripped for matching
- Case-insensitive matching (we = We = WE)

### Tree Building
- Context window: 5 words before/after root
- Hierarchical aggregation with occurrence counting
- Metadata attached at each node level
- Trees sorted by occurrence count (most common first)

### Color Coding Options

Use the metadata to color branches by:
- **Era**: Assign colors to historical periods
- **Speaker**: Highlight contributions from specific presidents
- **Frequency**: Gradient based on occurrence count

### Interactive Features

- Toggle between "after" and "before" directions
- Filter by era or speaker
- Expand/collapse tree branches
- Hover for details (full phrase, metadata)
- Search for specific word sequences
