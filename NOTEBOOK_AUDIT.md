# ContextKeeper Notebook -- Complete Feature Audit

**Date:** 2026-04-13
**Auditor:** Claude (Anthropic) + Steven Wazlavek
**Monolith:** monolith-source/public_html/data-lab.html (15,403 lines)
**Modern Port:** apps/agent-canvas/src/ (4,118 lines across 18 files)

---

## 1. Cell Types (12 types)

| Type | ID | Editor | Execution Engine | Status |
|------|----|--------|-----------------|--------|
| Python Code | `code` | Monaco (python) | Kernel Gateway (Jupyter) | Ported |
| Markdown | `md` | Monaco (markdown) | Client-side render | Ported |
| SQL | `sql` | Monaco (sql) | Kernel (via sql.js/sqlalchemy) | Ported |
| JavaScript | `js` | Monaco (javascript) | Browser eval / Kernel | Ported |
| Visualization | `viz` | Custom config UI | Plotly/Vega | Type defined, component stub |
| Form | `form` | Custom widget builder | N/A (UI only) | Type defined |
| Raw | `raw` | Monaco (plaintext) | No execution | Ported |
| Scratch | `scratch` | Monaco (plaintext) | No execution | Type defined |
| LaTeX | `latex` | Monaco (latex) | KaTeX render | Type defined |
| Mermaid | `mermaid` | Monaco (markdown) | Mermaid.js render | Type defined |
| HTML | `html` | Monaco (html) | iframe sandbox | Type defined |
| Prompt | `prompt` | Monaco (plaintext) | LLM via @ck/ai | Type defined |

---

## 2. Keyboard Shortcuts

### Global (always active)
- `Ctrl+S` -- manual save
- `Ctrl+Shift+P` -- command palette
- `Ctrl+B` -- toggle sidebar
- `Escape` -- enter command mode
- `Enter` -- enter edit mode (when command mode + cell active)

### Command Mode (single-key, Jupyter-compatible)
- `A` -- insert code cell above
- `B` -- insert code cell below
- `DD` -- delete cell (double-tap)
- `Y` -- change to code type
- `M` -- change to markdown type
- `Shift+M` -- merge with cell below
- `K` / `ArrowUp` -- navigate to cell above
- `J` / `ArrowDown` -- navigate to cell below
- `C` -- copy cell to clipboard
- `V` -- paste cell below
- `X` -- cut cell
- `Z` -- undo
- `Shift+Enter` -- run cell and advance

### Edit Mode (modifier+key)
- `Shift+Enter` -- run cell and advance to next
- `Ctrl+Enter` -- run cell and stay
- `Alt+Enter` -- run cell and insert new cell below

---

## 3. Command Palette Commands (22 commands)

### Cell Operations (11)
- Insert Code Cell Above / Below
- Insert Markdown Cell Below
- Insert SQL Cell Below
- Delete Cell
- Move Cell Up / Down
- Change Cell to Code / Markdown
- Merge Cell Below
- Clear Cell Outputs / Clear All Outputs

### Execution (4)
- Run Cell (Ctrl+Enter)
- Run Cell and Advance (Shift+Enter)
- Run Cell and Insert Below (Alt+Enter)
- Run All Cells

### Export (8 formats)
- Export as Python (.py)
- Export as Jupyter Notebook (.ipynb)
- Export as Markdown (.md)
- Export as HTML
- Export as PDF (via HTML)
- Export as LaTeX (.tex)
- Export as Slides (reveal.js)
- Export as DOCX (Pandoc)

### Modes (5)
- Normal Mode / Focus Mode / Zen Mode / Presentation Mode / Pipeline Mode

---

## 4. Notebook Modes (5)

| Mode | Topbar | Sidebar | StatusBar | CellToolbars | AddCellBars | FullWidth | SlideView |
|------|--------|---------|-----------|-------------|-------------|-----------|-----------|
| Normal | Y | Y | Y | Y | Y | N | N |
| Focus | Y | N | Y | Y | Y | N | N |
| Zen | N | N | N | N | N | Y | N |
| Presentation | N | N | N | N | N | Y | Y |
| Pipeline | Y | Y | Y | Y | N | N | N |

---

## 5. Store State (notebook-store.ts, 341 lines)

### Data
- `cells: Cell[]`
- `activeCellId: string | null`
- `selectedCellIds: Set<string>`
- `cellStatuses: Map<string, CellStatus>` (idle/running/queued/error)

### CRUD Actions (16)
- addCell, deleteCell, updateCellSource, updateCellType
- updateCellOutputs, updateCellMetadata, setCellExecutionCount
- moveCell, moveCellToIndex, mergeCells
- setActiveCell, toggleCellSelection, selectAllCells
- clearOutputs (single cell or all)
- setCells (bulk replace)
- clearNotebook

### History
- Undo/redo with snapshot stack (50 max)
- Per-cell version tracking (cell-history.ts)

---

## 6. Execution Service (notebook-execute.ts, 144 lines)

- `executeCell(cellId)` -- sends source to kernel, streams output
- `runAndAdvance(cellId)` -- execute + move to next cell
- `runAndStay(cellId)` -- execute + keep focus
- `runAndInsertBelow(cellId)` -- execute + create new cell below
- Execution time tracking (start/end timestamps)
- Status updates: idle -> queued -> running -> idle/error
- Queue-based execution (cell-execution.ts, 98 lines)

---

## 7. Save/Load System (notebook-save.ts, 319 lines)

- Auto-save to localStorage every 30 seconds when dirty
- Manual save via Ctrl+S
- Server persistence via POST /api/v1/notebooks
- Dirty flag tracking (any cell change sets dirty)
- Notebook title: editable in Topbar, persisted separately
- Save status: "Saved Xs ago" display in Topbar
- Import .ipynb files (notebook-import.ts, 328 lines)
  - Parses nbformat v4 JSON
  - Maps cell types: code, markdown, raw
  - Imports outputs with MIME type handling
  - Clipboard paste detection for notebook JSON

---

## 8. Export Formats (notebook-export.ts, 410 lines)

1. **Python (.py)** -- `# %%` cell markers, markdown as comments
2. **Jupyter (.ipynb)** -- full nbformat v4.5 with outputs, MIME data
3. **Markdown (.md)** -- cells as sections, code in fenced blocks
4. **HTML** -- styled document with code highlighting
5. **PDF** -- via HTML-to-print
6. **LaTeX (.tex)** -- lstlisting for code, standard sections
7. **Slides (reveal.js)** -- one slide per cell, horizontal slides
8. **DOCX** -- via Pandoc-compatible markdown

---

## 9. Cell Operations Library (cell-operations.ts, 244 lines)

32 functions matching monolith NB.* namespace:
- addCell, addCellAt, deleteCell, undoDelete
- copyCell, cutCell, pasteCell
- duplicateCell, splitCell, mergeCellBelow
- moveUp, moveDown, moveToTop, moveToBottom
- toggleCellType (code/md/sql/js cycle)
- selectAll, deselectAll, selectRange
- collapseCell, expandCell, toggleCollapse
- lockCell, unlockCell
- clearOutput, clearAllOutputs
- runAbove, runBelow, runAll
- findReplace (within cell source)
- insertSnippet (template insertion)

---

## 10. Output Types Handled (4)

| Type | Description | Rendering |
|------|-------------|-----------|
| `stream` | stdout/stderr text | Pre-formatted text, color-coded |
| `execute_result` | Rich display data | MIME-type dispatch |
| `display_data` | Rich display (images, HTML, plots) | MIME-type dispatch |
| `error` | Exception traceback | Red text with ANSI parsing |

### MIME Types (CellOutput.tsx)
- `text/plain` -- monospace pre
- `text/html` -- sandboxed iframe
- `image/png` / `image/jpeg` / `image/svg+xml` -- img tag
- `application/json` -- interactive JSON tree
- DataFrame detection -- routes to DataFrameRenderer

---

## 11. DataFrameRenderer (276 lines)

Interactive table with:
- Column sort (click header: asc/desc/none)
- Column filter (text input per column)
- Pagination (10/25/50/100 rows per page)
- Column statistics (count, mean, std, min, max, unique)
- Row count display
- Export to CSV button
- Copy to clipboard button
- Scrollable with sticky header
- Observatory dark theme

---

## 12. Between-Cell Menu (BetweenCellMenu.tsx, 188 lines)

Hover-activated "+" button between cells:
- Insert Code / Markdown / SQL / JS cell
- Insert from snippet library (8 built-in snippets)
- Insert from template
- AI Generate cell (LLM prompt to generate code)

---

## 13. Cell Toolbar (CellToolbar.tsx, 215 lines)

Per-cell floating toolbar (visible on hover):
- Cell type badge (Code/Markdown/SQL/JS)
- Language selector dropdown
- Execution count display [N]
- Run button (play icon)
- Move up/down arrows
- Delete button (trash icon)
- More menu: duplicate, split, merge, collapse, lock, copy/cut

---

## 14. Page Component (NotebookPage.tsx, 251 lines)

Wiring layer:
- Renders cell list with drag-and-drop reordering
- Between-cell menus
- Keyboard shortcut registration on mount
- Auto-save initialization
- Mode subscription
- Active cell scroll-into-view

---

## 15. Monolith Features NOT Yet Ported

From data-lab.html (15,403 lines):
- Voice-to-code (CK_Voice) -- mic button on every textarea
- Text-to-speech (CK_Speak) -- read cell output aloud
- Pyodide in-browser execution fallback
- sql.js in-browser SQLite
- IndexedDB workspace file cache
- Observability panel (ck-observe.1.0.js, 30KB)
- Universal AI call layer (ck-universal.js, 30KB)
- File browser panel (ck-files.1.0.js, 25KB)
- Data engine (ck-data.1.0.js, 18KB) with DataFrame ops
- Monaco editor management layer (ck-editor.1.0.js, 6KB)
- Core engine (ck-core.1.0.js, 56KB) shared across all tools
- Collaborative editing hints
- Cell-level execution metrics
- Variable explorer integration
- Inline data profiling
- Chart recommendation engine

---

## 16. File Inventory

| Category | Files | Lines |
|----------|-------|-------|
| Monolith data-lab.html | 1 | 15,403 |
| Monolith JS libraries | 6 | ~7,000 est |
| Modern notebook features | 7 | 2,246 |
| Modern cell components | 7 | 988 |
| Modern cell utilities | 3 | 371 |
| Modern page component | 1 | 251 |
| Modern shared types | 1 | ~120 |
| Backend (models/schemas/service/router) | 4 | 344 |
| **Modern Total** | **23** | **4,320** |
| **Monolith Total** | **7** | **~22,400** |

---

## 17. Feature Count Summary

- Cell types: 12 (5 fully ported, 7 type-defined)
- Keyboard shortcuts: 18 bindings
- Command palette commands: 22
- UI modes: 5
- Store actions: 16
- Cell operations: 32
- Export formats: 8
- Output types: 4
- MIME types: 6
- Between-cell menu items: 4 categories
- Toolbar actions: 10+

**Total discrete features: 137**
