# Presidential Speech Word Tree Visualization

Interactive D3.js visualization for exploring word sequences in presidential speeches.

## Features

- **Interactive Collapsible Tree**: Click nodes to expand/collapse branches
- **Root Word Selection**: Explore 5 different root words (we, must, freedom, fear, never)
- **Bidirectional Analysis**: Toggle between suffix (after) and prefix (before) analysis
- **Color Coding**: View by historical era or speaker (president)
- **Filtering**: Filter tree branches by era or speaker
- **Search & Highlight**: Find and highlight specific words in the tree
- **Tooltips**: Hover over nodes for detailed statistics
- **Smooth Animations**: 750ms transitions between states

## Quick Start

### Option 1: Using Python's Built-in HTTP Server

```bash
# From the word-tree directory
python3 -m http.server 8000
```

Then open your browser to: `http://localhost:8000`

### Option 2: Using Node.js http-server

```bash
# Install http-server globally (if not installed)
npm install -g http-server

# From the word-tree directory
http-server -p 8000
```

Then open your browser to: `http://localhost:8000`

### Option 3: Using VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## File Structure

```
word-tree/
├── index.html              # Main HTML page
├── css/
│   └── style.css          # Styling
├── js/
│   ├── utils.js           # Utility functions
│   ├── tree.js            # D3.js tree visualization
│   ├── controls.js        # UI controls
│   └── main.js            # Application logic
├── data/
│   ├── metadata.json      # Global metadata (1.55 KB)
│   ├── we.json           # "we" root word data (92.93 MB)
│   ├── must.json         # "must" root word data (18.28 MB)
│   ├── freedom.json      # "freedom" root word data (6.11 MB)
│   ├── fear.json         # "fear" root word data (1.54 MB)
│   └── never.json        # "never" root word data (7.03 MB)
```

## Usage

### Controls

1. **Root Word Selector**: Choose which root word to analyze
2. **Direction Toggle**: Switch between "After (Suffix)" and "Before (Prefix)"
3. **Color By**: Toggle between "Historical Era" and "Speaker (President)"
4. **Filter By**: Restrict visible branches to a selected era or speaker
5. **Search**: Enter a word to highlight matching nodes
6. **Expand/Collapse All**: Quick controls for tree exploration

### Interactions

- **Click nodes**: Expand or collapse child branches
- **Hover nodes**: View detailed statistics in tooltip
- **Search**: Find specific words and highlight all occurrences

### Color Coding

**By Era** (Sequential gradient):
- Blue tones: Early eras (Founding, Jacksonian, Civil War)
- Purple tones: Middle eras (Gilded Age, Progressive)
- Red/Orange tones: Modern eras (Cold War, Post-Cold War, Modern)

**By Speaker**: Each president gets a consistent color based on their name

## Data Details

### Root Words Analyzed

| Root Word | After Tree Nodes | Before Tree Nodes | Data File Size |
|-----------|-----------------|-------------------|----------------|
| we        | 113,290         | 131,471          | 92.93 MB       |
| must      | 23,705          | 24,809           | 18.28 MB       |
| freedom   | 8,224           | 8,111            | 6.11 MB        |
| fear      | 2,104           | 2,075            | 1.54 MB        |
| never     | 9,613           | 9,339            | 7.03 MB        |

### Historical Eras

1. Founding Era (1789-1828)
2. Jacksonian Era (1829-1860)
3. Civil War & Reconstruction (1861-1877)
4. Gilded Age (1878-1900)
5. Progressive Era (1901-1920)
6. Roaring 20s & Depression (1921-1945)
7. Cold War (1946-1991)
8. Post-Cold War (1992-2001)
9. Modern Era (2001-present)

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

Requires modern browser with ES6+ support and D3.js v7.

## Technical Stack

- **D3.js v7**: Tree layout and visualization
- **Vanilla JavaScript**: No build tools required
- **CSS3**: Modern styling with animations
- **HTML5**: Semantic markup

## Example Insights

**"We have"** (5,894 occurrences)
- Top era: Cold War (2,359)
- Top speakers: Lyndon B. Johnson (881), Donald Trump (753)

**"Freedom is"** (114 occurrences)
- Common sequences: "freedom is not", "freedom is a"

**"Never forget"** (frequent phrase)
- Spans multiple eras
- Used by various presidents

## Credits

Data source: Miller Center Presidential Speeches (1,056 speeches from 45 presidents, 1789-2026)
