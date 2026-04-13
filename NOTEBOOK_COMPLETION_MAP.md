# Notebook Completion Map

**Date:** 2026-04-13
**Total files audited:** 24 notebook-specific TypeScript files (4,146 lines)
**Overall completion: ~55% of standard notebook features, ~5% of novel features**

---

## Files Found (24 files, 4,146 lines)

| File | Lines | Category |
|------|-------|----------|
| notebook-keyboard.ts | 500 | Feature module |
| notebook-export.ts | 410 | Feature module |
| notebook-store.ts | 341 | Feature module |
| notebook-import.ts | 328 | Feature module |
| notebook-save.ts | 319 | Feature module |
| notebook-modes.ts | 204 | Feature module |
| notebook-execute.ts | 144 | Feature module |
| kernel-client.ts | 412 | Library |
| cell-operations.ts | 244 | Library |
| cell-execution.ts | 98 | Library |
| cell-history.ts | 29 | Library |
| DataFrameRenderer.tsx | 276 | Cell component |
| Cell.tsx | 236 | Cell component |
| CellToolbar.tsx | 215 | Cell component |
| BetweenCellMenu.tsx | 188 | Cell component |
| MarkdownCell.tsx | 111 | Cell component |
| CellOutput.tsx | 91 | Cell component |
| CodeCell.tsx | 71 | Cell component |
| SqlCell.tsx | 62 | Cell component |
| CellListPanel.tsx | 153 | Sidebar |
| NotebookPage.tsx | 251 | Page |
| types.ts | ~120 | Types |
| index.ts (cells) | 10 | Barrel |

---

## Status by Component

### COMPLETE (fully working, no changes needed) -- 26 features

- **notebook-store.ts** -- Zustand store with 16 CRUD actions, undo/redo (50 snapshots), active cell, multi-select, cell statuses
- **notebook-keyboard.ts** -- 18 keyboard shortcuts (command mode A/B/DD/Y/M/K/J/C/V/X/Z, edit mode Shift/Ctrl/Alt+Enter, global Ctrl+S/Ctrl+Shift+P/Ctrl+B/Escape/Enter), 22 command palette commands
- **notebook-execute.ts** -- runAndAdvance, runAndStay, runAndInsertBelow, executeCell with timing
- **notebook-save.ts** -- localStorage auto-save (30s), manual Ctrl+S, server persistence, dirty tracking, title management
- **notebook-export.ts** -- 8 formats: .py, .ipynb (nbformat v4.5 with outputs), .md, .html, .pdf, .tex, slides, .docx
- **notebook-import.ts** -- .ipynb import with output/MIME preservation, clipboard paste detection
- **notebook-modes.ts** -- 5 UI modes (normal, focus, zen, presentation, pipeline) with per-mode config
- **kernel-client.ts** -- WebSocket to Jupyter Kernel Gateway, execute with streaming outputs, reconnect, interrupt, status events
- **cell-operations.ts** -- 32 NB.* functions: full CRUD, clipboard, move, merge, split, collapse, lock, find/replace
- **cell-execution.ts** -- Queue-based execution with progress tracking
- **cell-history.ts** -- Per-cell version snapshots, restore, dedup
- **Cell.tsx** -- Dispatcher component, drag-and-drop reorder, click-to-select, active border, status indicators, execution time badge
- **CodeCell.tsx** -- Monaco editor + output area, language mapping (Python/JS/SQL/HTML), execution count badge, locked state
- **SqlCell.tsx** -- Monaco SQL editor + table output
- **CellOutput.tsx** -- Output dispatcher: stream (stdout/stderr), execute_result, display_data, error. MIME: text/plain, text/html (sanitized), image/png, image/svg+xml, DataFrame detection
- **DataFrameRenderer.tsx** -- Sort, filter, paginate (10/25/50/100), column stats, row count, export CSV, copy clipboard, Observatory dark theme
- **CellToolbar.tsx** -- Type badge, language selector, execution count, run/move/delete/duplicate, more menu (split, merge, collapse, lock, copy/cut), metadata toggles
- **BetweenCellMenu.tsx** -- Insert code/markdown/SQL/JS, snippet library (8 built-in), template insert, AI generate cell
- **NotebookPage.tsx** -- Full wiring: store, execution, keyboard, save, kernel, drag-and-drop
- **CellListPanel.tsx** -- Sidebar cell list with type badges and preview snippets

### PARTIAL (exists but needs work) -- 6 features

1. **MarkdownCell.tsx** -- Edit mode (Monaco) works. Preview mode uses a SIMPLE line-by-line renderer (headings, bullets, code fences as `<hr>`). **Missing:** RenderedOutput integration for full markdown+KaTeX rendering. The comment on line 5 explicitly says "A full markdown renderer will be added in a later task."

2. **Cell type dispatch** -- Cell.tsx handles code/js/html (CodeCell), md/latex (MarkdownCell), sql (SqlCell). Default fallback shows raw source in `<pre>`. **Missing:** Dedicated components for: viz, form, scratch, mermaid, html (sandboxed iframe), prompt, latex (KaTeX block render).

3. **Drag-and-drop** -- Cell.tsx has drag handles and onDragOver/onDrop. **Missing:** Visual drop indicator (highlight line between cells), smooth animation during drag.

4. **BetweenCellMenu AI Generate** -- Button exists. **Missing:** Actual LLM integration (needs to call sendMessage and insert generated code as new cell).

5. **notebook-modes.ts** -- Mode configs defined. **Missing:** Presentation mode slide navigation (next/prev slide, slide counter, full-screen toggle). Pipeline mode linear flow view not implemented.

6. **Server persistence** -- notebook-save.ts has server save/load code. **Missing:** Authentication context (isAuthenticated check), actual notebook list/open/delete UI, share by link.

### MISSING (needed but not yet built) -- 14 features

1. **VizCell component** -- For `viz` cell type. Needs: Plotly/Vega config UI, chart type picker, column mapping, auto-chart recommendation.

2. **FormCell component** -- For `form` cell type. Needs: widget builder (slider, dropdown, date picker, text input, button, file upload), reactive binding to downstream cells.

3. **MermaidCell component** -- For `mermaid` type. Needs: Mermaid.js integration, live preview, export to SVG/PNG.

4. **PromptCell component** -- For `prompt` type. Needs: LLM model selector, system prompt, user prompt, streaming output, cost display.

5. **HTMLCell component** -- For `html` type. Needs: sandboxed iframe rendering, CSP policy, resize handles.

6. **Variable explorer** -- Sidebar panel showing all kernel variables with type, shape, size. Click to inspect. Exists in monolith (ck-data.1.0.js) but not ported.

7. **Inline data profiling** -- Per-DataFrame cell: show column types, null counts, distributions. Exists in monolith.

8. **Run All / Run Above / Run Below** -- Buttons and commands exist in cell-operations.ts. Missing: UI buttons in toolbar, progress indicator for multi-cell execution.

9. **Notebook metadata panel** -- Title, author, description, tags, kernel spec, created/modified dates. Stored but no editor UI.

10. **TOC / Outline panel** -- Auto-generated from markdown headings. Navigate by clicking. Exists in monolith.

11. **Search and replace** -- Within notebook (across all cells). findReplace exists in cell-operations.ts but no UI.

12. **Execution queue visualization** -- Show which cells are queued, running, pending. Status bar indicator.

13. **Pyodide fallback** -- Browser-based Python execution when kernel is unavailable. Exists in monolith (ck-data.1.0.js).

14. **Multi-kernel support** -- Python + R + Julia in same notebook. Currently single Python kernel only.

### NOVEL (from NOTEBOOK_ARCHITECTURE.md -- entirely new features)

1. **Living Pipeline / Continuous Execution Mode** -- Cells re-execute automatically when upstream changes. Reactive mode (Marimo-style). Needs: dependency graph tracking, change detection, auto-re-execution engine.

2. **Branch Cells** -- Create parallel alternative cells (4A/4B). Both receive identical input, execute in parallel. Needs: branch creation UI, parallel execution engine, visual branch indicators.

3. **Statistical Comparison Layer** -- Compare branch outputs with hypothesis tests: paired t-test, McNemar's, Wilcoxon, Diebold-Mariano, DeepEval metrics. Needs: stats engine, comparison results UI, significance indicators.

4. **Auto-Replace System** -- Winner replaces loser after statistical significance reached. 4 replace modes: auto, notify, suggest, never. Needs: replacement engine, approval gate UI, configuration panel.

5. **Cell Contracts** -- Input/output schema validation (Pandera + Pydantic). Contract editor UI, violation indicators, contract inheritance for branches.

6. **Tournament Cell** -- N methods compete, pick winner. Different from Model Tournament (which compares LLM models). This compares arbitrary code cells.

7. **Agent Cell** -- Runs an Agent Canvas pipeline as a single cell. Bidirectional sync between notebook and canvas.

8. **Decision/Router Cell** -- Conditional routing based on output shape/values. If/else branching in the pipeline.

9. **Scheduled Execution** -- Cron-based pipeline runs. Needs: cron expression editor, schedule management UI, run history.

10. **Event-Driven Execution** -- Trigger on webhook, file change, API call, data arrival. Needs: event source configuration, webhook endpoint.

11. **Streaming Execution** -- Row-by-row processing (Kafka/Flink style). Needs: streaming adapter, backpressure handling.

12. **Fine-Tune Cell** -- Dataset builder + training job + model eval as notebook cells. Partially exists via FineTunePanel but not as cell type.

13. **Voice-to-Code** -- Mic button on every code cell. Exists in monolith (CK_Voice in ck-universal.js) but not ported.

14. **Notebook-Canvas Sync** -- Pin notebook cells as Agent Canvas nodes and vice versa. Changes sync bidirectionally.

---

## Build Order Recommendation

### Phase 1: Complete Standard Notebook (est. 800 lines)
1. **MarkdownCell RenderedOutput integration** -- swap simple preview for RenderedOutput component (already built in Sprint 2). ~30 lines changed.
2. **BetweenCellMenu AI Generate** -- wire sendMessage, insert generated code. ~50 lines.
3. **Run All / Run Above / Run Below buttons** -- add to toolbar. ~40 lines.
4. **PromptCell component** -- LLM cell with model selector and streaming. ~150 lines.
5. **VizCell component** -- Plotly config UI. ~200 lines.
6. **MermaidCell component** -- Mermaid.js live preview. ~80 lines.
7. **Variable explorer panel** -- kernel variable inspection. ~150 lines.
8. **Search and replace UI** -- modal with find/replace across cells. ~100 lines.

### Phase 2: Novel Core Features (est. 2,500 lines)
1. **Reactive execution mode** -- dependency graph + auto-re-execute. ~400 lines.
2. **Branch cells** -- parallel alternatives with split/merge UI. ~500 lines.
3. **Statistical comparison** -- hypothesis testing engine + results UI. ~400 lines.
4. **Cell contracts** -- schema editor + validation engine. ~300 lines.
5. **Agent cell** -- Agent Canvas integration as cell. ~200 lines.
6. **Decision/router cell** -- conditional branching. ~150 lines.
7. **Tournament cell** -- N-way method comparison. ~250 lines.
8. **Fine-tune cell** -- wrap FineTunePanel as cell. ~150 lines.
9. **Notebook-Canvas sync** -- bidirectional pin/sync. ~150 lines.

### Phase 3: Production Features (est. 1,200 lines)
1. **Scheduled execution** -- cron + management UI. ~300 lines.
2. **Pyodide fallback** -- browser Python when kernel unavailable. ~400 lines.
3. **Voice-to-code** -- Web Speech API + mic buttons. ~200 lines.
4. **Multi-kernel** -- kernel selector per cell. ~300 lines.

---

## Estimated Lines of New Code

| Phase | Est. Lines | Priority |
|-------|-----------|----------|
| Phase 1: Complete Standard | 800 | HIGH -- unblocks daily use |
| Phase 2: Novel Core | 2,500 | HIGH -- differentiator features |
| Phase 3: Production | 1,200 | MEDIUM -- production readiness |
| **Total** | **4,500** | |

Current: 4,146 lines. After all phases: ~8,646 lines.
