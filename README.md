# Presidential Speech Word Tree Analysis

Python-based tokenization and data processing system for analyzing 1,056 presidential speeches and creating interactive word tree visualizations.

## Overview

This project analyzes presidential speeches to build hierarchical word trees showing word sequences that follow (or precede) specific root words. The output is formatted for D3.js visualization with metadata for color coding by historical era or speaker.

## Features

- **Bidirectional Analysis**: Track words both before and after root words
- **Historical Context**: Speeches categorized into 9 historical eras
- **Case-Insensitive Matching**: Captures all variations of root words
- **Rich Metadata**: Era and speaker distributions at each tree node
- **D3.js Ready**: Output formatted for hierarchical D3.js layouts

## Dataset

- **1,056 speeches** from 45 U.S. presidents
- Date range: 1789-04-30 to 2026-02-28
- Speeches include inaugurals, State of the Union addresses, major policy speeches, etc.

## Root Words Analyzed

1. **we** - 113,290 nodes (after), 131,471 nodes (before)
2. **must** - 23,705 nodes (after), 24,809 nodes (before)
3. **freedom** - 8,224 nodes (after), 8,111 nodes (before)
4. **fear** - 2,104 nodes (after), 2,075 nodes (before)
5. **never** - 9,613 nodes (after), 9,339 nodes (before)

## Historical Eras

- Founding Era (1789-1828)
- Jacksonian Era (1829-1860)
- Civil War & Reconstruction (1861-1877)
- Gilded Age (1878-1900)
- Progressive Era (1901-1920)
- Roaring 20s & Depression (1921-1945)
- Cold War (1946-1991)
- Post-Cold War (1992-2001)
- Modern Era (2001-present)
