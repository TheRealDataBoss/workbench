# ContextKeeper Platform Architecture Map

**Generated:** 2026-04-12
**Source:** Full file-system audit of contextkeeper-platform monorepo + workbench cross-reference
**Author:** Steven Wazlavek + Claude (Anthropic)

---

## 1. Monorepo Structure

```
contextkeeper-platform/                    # Root -- pnpm 9.15.4 + Turborepo 2.9
|-- package.json                           # Workspace root, scripts: build/dev/lint/typecheck/clean
|-- pnpm-workspace.yaml                    # Workspaces: apps/*, packages/@ck/*, tooling/*
|-- turbo.json                             # Turborepo task config (build, dev, typecheck, lint, test, clean)
|-- tsconfig.base.json                     # Shared TS config: ES2022 target, strict mode, react-jsx
|-- pnpm-lock.yaml                         # 207KB lockfile
|-- .npmrc                                 # pnpm config
|-- Makefile                               # dev/build/test/lint/deploy shortcuts
|-- CLAUDE.md                              # AI assistant project rules
|-- CONTRIBUTING.md                        # Dev setup, code standards, test instructions
|-- DEPLOYMENT.md                          # Server setup, env vars, systemd, SSL, CI/CD
|-- SHORTCUTS.md                           # Keyboard shortcut reference
|-- README.md                              # Project overview
|-- LICENSE                                # License file
|
|-- apps/
|   |-- data-canvas/                       # PRIMARY APP -- the main ContextKeeper IDE
|   |   |-- src/                           # 267 TS/TSX files, 69,959 lines
|   |   |   |-- api/                       # API client layer
|   |   |   |-- assets/                    # Static assets
|   |   |   |-- components/                # React components
|   |   |   |   |-- analytics/             # 28 Plotly chart components (ROC, SHAP, confusion matrix, etc.)
|   |   |   |   |-- cell/                  # Notebook cell components (8 files + barrel)
|   |   |   |   |-- editor/                # Monaco editor wrapper + theme (3 files)
|   |   |   |   |-- layout/                # Sidebar, Topbar, StatusBar (4 files)
|   |   |   |   |-- terminal/              # 28 terminal components (engine, tabs, panels, AI, git, etc.)
|   |   |   |   |-- ui/                    # Shared UI: CommandPalette, Modal, Toast, PortalDropdown, Voice
|   |   |   |   |-- AgentDetailPanel.tsx
|   |   |   |   |-- AnalyticsPanel.tsx
|   |   |   |   |-- BottomPanel.tsx
|   |   |   |   |-- CanvasToolbar.tsx
|   |   |   |   |-- ConsolePanel.tsx
|   |   |   |   |-- ContextMenu.tsx
|   |   |   |   |-- NodeDetailPanel.tsx
|   |   |   |   |-- NodeSidebar.tsx         # DO NOT TOUCH (per CLAUDE.md)
|   |   |   |   |-- PropertiesPanel.tsx
|   |   |   |   |-- SettingsPanel.tsx
|   |   |   |-- edges/                     # React Flow edge types
|   |   |   |-- engine/                    # Pipeline execution engine
|   |   |   |   |-- llmRunner.ts           # LLM node execution
|   |   |   |   |-- pipelineRunner.ts      # Full pipeline orchestration
|   |   |   |   |-- resultExtractor.ts     # Output extraction
|   |   |   |   |-- singleNodeRunner.ts    # Single node execution
|   |   |   |   |-- topologicalSort.ts     # DAG topological sort
|   |   |   |-- features/                  # Feature modules
|   |   |   |   |-- ai/                    # AiActions.ts, AiChat.tsx
|   |   |   |   |-- bridges/               # cross-tool-bridge.ts
|   |   |   |   |-- canvas/                # CanvasEdge, CanvasNode, CanvasToolbar, canvas-store, node-registry
|   |   |   |   |-- notebook/              # 7 notebook feature modules (see Section 3)
|   |   |   |   |-- sidebar/               # 42 sidebar panel components
|   |   |   |       |-- (root)/            # CellListPanel, ConnectorsPanel, FilesPanel, etc. (11 files)
|   |   |   |       |-- canvas/            # AutoML, CodeReview, DataQuality, Lineage, etc. (15 files)
|   |   |   |       |-- terminal/          # AIChat, Debug, Docs, History, SSH, etc. (12 files)
|   |   |   |-- hooks/                     # Custom React hooks
|   |   |   |-- layouts/                   # Layout wrappers
|   |   |   |-- lib/                       # Utilities (18 files)
|   |   |   |   |-- api-client.ts          # HTTP client
|   |   |   |   |-- auth.ts                # Auth helpers
|   |   |   |   |-- cell-execution.ts      # Cell execution queue (98 lines)
|   |   |   |   |-- cell-history.ts        # Per-cell version tracking (29 lines)
|   |   |   |   |-- cell-operations.ts     # 32 cell CRUD functions (244 lines)
|   |   |   |   |-- canvas-command-registry.ts
|   |   |   |   |-- cm-ghost-completion.ts # CodeMirror ghost text
|   |   |   |   |-- command-registry.ts    # Command palette registry
|   |   |   |   |-- dataframe-utils.ts     # DataFrame utilities
|   |   |   |   |-- event-bus.ts           # Event bus
|   |   |   |   |-- feature-flags.ts       # Feature flag system
|   |   |   |   |-- kernel-client.ts       # Jupyter Kernel Gateway WebSocket client (412 lines)
|   |   |   |   |-- layout-nodes.ts        # Node layout helpers
|   |   |   |   |-- modelRegistry.ts       # AI model registry
|   |   |   |   |-- sanitize.ts            # HTML sanitization
|   |   |   |   |-- types.ts               # Shared types (~120 lines)
|   |   |   |   |-- voice-input.ts         # Voice input helpers
|   |   |   |   |-- aiNodeFeatures.ts      # AI node feature helpers
|   |   |   |-- nodes/                     # Data Canvas node system (45 files)
|   |   |   |   |-- nodeRegistry.ts        # 1,694 lines -- DO NOT TOUCH (per CLAUDE.md)
|   |   |   |   |-- DataCanvasNode.tsx      # Main node component
|   |   |   |   |-- AgentCanvasNode.tsx     # Agent canvas node variant
|   |   |   |   |-- NodeHeaderExtras.tsx
|   |   |   |   |-- data/                  # Node data: contracts, profiles, chart routing, etc. (7 files)
|   |   |   |   |-- sections/              # Node detail sections: AI, Code, Compute, Data, etc. (20+ files)
|   |   |   |-- pages/                     # Route pages (10 files)
|   |   |   |   |-- NotebookPage.tsx       # Notebook view (251 lines)
|   |   |   |   |-- DataCanvasPage.tsx     # Data Canvas (React Flow)
|   |   |   |   |-- DataCanvasFlow.tsx     # Canvas flow renderer
|   |   |   |   |-- AgentCanvasPage.tsx    # Agent Canvas
|   |   |   |   |-- AgentCanvasFlow.tsx    # Agent Canvas flow renderer
|   |   |   |   |-- IdePage.tsx            # IDE/code editor page
|   |   |   |   |-- TerminalPage.tsx       # Terminal page
|   |   |   |   |-- ChatPage.tsx           # Chat interface
|   |   |   |   |-- ConnectorsPage.tsx     # Data connectors
|   |   |   |   |-- VizStudioPage.tsx      # Visualization studio
|   |   |   |-- routes/                    # React Router config
|   |   |   |-- stores/                    # Zustand stores
|   |   |   |   |-- canvasStore.ts         # Data Canvas state
|   |   |   |   |-- agentCanvasStore.ts    # Agent Canvas state
|   |   |   |   |-- terminalStore.ts       # Terminal state
|   |   |   |-- styles/                    # Observatory CSS tokens
|   |   |   |-- templates/                 # Pipeline templates (1 file)
|   |   |   |-- viz-studio/                # Viz Studio module (15 files)
|   |   |       |-- VizStudio.tsx          # Main viz studio component
|   |   |       |-- VizStudioMini.tsx      # Mini variant
|   |   |       |-- data/                  # chartTypes, colorPalettes, plotlyChartBuilder
|   |   |       |-- panels/               # 9 panels: AI, Analytics, Annotation, Axes, Chart, etc.
|   |   |       |-- store/                # vizStore.ts
|   |   |-- tests/                         # 17 Vitest test files
|   |   |-- vite.config.ts                 # Vite build config
|   |   |-- tailwind.config.ts
|   |   |-- tsconfig.json
|   |
|   |-- agent-canvas/                      # SECONDARY APP -- Agent Canvas standalone (scaffolded)
|       |-- src/                           # 285 TS/TSX files, 2,177 lines (mostly stubs)
|       |-- vite.config.ts
|       |-- tsconfig.json
|
|-- packages/
|   |-- @ck/
|       |-- ai/                            # AI client library
|       |   |-- src/browser.ts             # Browser-side AI client
|       |   |-- src/client.ts              # Server-side AI client
|       |   |-- src/models.ts              # Model definitions
|       |   |-- src/puter-types.d.ts       # Puter type declarations
|       |   |-- src/index.ts               # Barrel export
|       |
|       |-- sync/                          # Real-time sync (Yjs/CRDT)
|       |   |-- src/index.ts               # Sync client
|       |
|       |-- types/                         # Shared TypeScript types
|       |   |-- src/index.ts               # Type barrel
|       |
|       |-- ui/                            # Shared UI components
|       |   |-- src/SidebarSection.tsx      # Canonical sidebar section primitive
|       |   |-- src/SidebarSectionStack.tsx # Sidebar section stack
|       |   |-- src/ResizeSash.tsx          # Resize sash component
|       |   |-- src/SectionDefaultOpenContext.ts
|       |   |-- src/index.ts               # Barrel export
|       |
|       |-- utils/                         # Shared utilities
|           |-- src/fuzzy-match.ts         # Fuzzy matching algorithm
|           |-- src/index.ts               # Barrel export
|
|-- shared/                                # Shared TypeScript type definitions (not a package)
|   |-- index.ts                           # Re-exports kernel, notebook, session
|   |-- notebook.ts                        # NotebookCell, NotebookDocument, CellOutput types (57 lines)
|   |-- kernel.ts                          # KernelInfo, KernelExecuteRequest/Reply types (25 lines)
|   |-- session.ts                         # SessionInfo, SessionEvent types (27 lines)
|   |-- tsconfig.json
|
|-- backend/                               # FastAPI Python backend
|   |-- app/                               # 4,891 lines of Python
|   |   |-- main.py                        # FastAPI entry point
|   |   |-- config.py                      # Settings via Pydantic
|   |   |-- database.py                    # SQLAlchemy async engine
|   |   |-- dependencies.py                # DI providers
|   |   |-- api/v1/                        # API router aggregator
|   |   |-- routers/                       # 13 endpoint modules
|   |   |   |-- auth.py, billing.py, browser.py, chat.py, connectors.py
|   |   |   |-- files.py, finetune.py, mcp.py, memory.py, notebooks.py
|   |   |   |-- optimize.py, pipeline_connectors.py, vectors.py, a2a.py
|   |   |-- services/                      # 6 business logic modules
|   |   |   |-- ai_service.py, auth_service.py, billing_service.py
|   |   |   |-- connector_service.py, file_service.py, notebook_service.py
|   |   |-- models/                        # 6 SQLAlchemy ORM models
|   |   |   |-- audit.py, connector.py, file.py, notebook.py, subscription.py, user.py
|   |   |-- schemas/                       # 6 Pydantic v2 schemas
|   |   |   |-- auth.py, billing.py, chat.py, connector.py, file.py, notebook.py
|   |   |-- middleware/                     # CORS, rate limiting, security
|   |   |-- connectors/                    # 30 data source implementations
|   |   |   |-- base.py (abstract), registry.py
|   |   |   |-- api_graphql.py, api_rest.py, arxiv_conn.py, azure_blob.py
|   |   |   |-- bigquery.py, crypto.py, csv_conn.py, elasticsearch.py
|   |   |   |-- gcs.py, github.py, google_drive.py, huggingface_conn.py
|   |   |   |-- json_conn.py, local_file.py, mongodb.py, mysql_conn.py
|   |   |   |-- parquet.py, postgresql.py, reddit_conn.py, redis_conn.py
|   |   |   |-- s3.py, sec_edgar.py, sftp.py, snowflake.py, sqlite_conn.py
|   |   |   |-- ssrf.py, wikipedia_conn.py, yahoo_finance.py
|   |   |-- utils/
|   |-- migrations/                        # Alembic DB migrations
|   |-- datasets/                          # Sample datasets
|   |-- finetuned_models/                  # Fine-tuned model storage
|   |-- tests/                             # pytest tests (conftest.py + .gitkeep)
|   |-- Dockerfile                         # Container build
|   |-- pyproject.toml                     # Python project config
|   |-- alembic.ini                        # Alembic config
|   |-- .env / .env.example                # Environment variables
|
|-- kernel-gateway/                        # Jupyter Kernel Gateway config
|
|-- electron-app/                          # Electron desktop wrapper
|
|-- electron/                              # Electron config/scripts
|
|-- deploy/                                # Deployment scripts (bash)
|
|-- infra/                                 # Infrastructure (PowerShell deploy)
|
|-- marketing/                             # Marketing site
|
|-- monolith-source/                       # Production monolith reference (gitignored)
|   |-- public_html/                       # ~60 files -- original ContextKeeper
|
|-- tooling/                               # 40 PowerShell audit/migration scripts
|
|-- docs/                                  # 2 Word documents
|   |-- ContextKeeper_Master_Roadmap.docx
|   |-- ContextKeeper_Platform_Architecture.docx
|
|-- .contextkeeper/                        # Internal planning docs
|   |-- DEPLOYMENT-PLAN-V3.md
|   |-- REWRITE-PLAN-V2.md
|   |-- REWRITE-PLAN.md
|
|-- .migration/                            # Migration tracking
|   |-- STATE.json, STATE-1.5.json, STATE-PHASE2.json
|   |-- CANVAS-FEATURE-AUDIT.md
|   |-- LAYOUT-AUDIT.md
|   |-- gate-check.mjs                    # Build gate check script
|   |-- tasks/                             # 25 migration task files (TASK-01 through TASK-17, TASK-P2-*)
|
|-- .github/                               # GitHub Actions CI/CD
|-- .turbo/                                # Turborepo cache
```

---

## 2. Current State

### Code Metrics

| Location | Files (TS/TSX) | Lines | Status |
|----------|---------------|-------|--------|
| apps/data-canvas/src/ | 267 | 69,959 | PRIMARY -- fully functional |
| apps/agent-canvas/src/ | 285 | 2,177 | Scaffolded stubs |
| packages/@ck/ai/src/ | 5 | ~200 est | Functional |
| packages/@ck/sync/src/ | 1 | ~50 est | Stub/minimal |
| packages/@ck/types/src/ | 1 | ~50 est | Stub/minimal |
| packages/@ck/ui/src/ | 5 | ~400 est | Functional (SidebarSection, ResizeSash) |
| packages/@ck/utils/src/ | 2 | ~100 est | Functional (fuzzy-match) |
| shared/ | 4 | 112 | Functional types |
| backend/app/ | ~80 .py | 4,891 | Functional |
| **Total modern code** | **~650** | **~78,000** | |

### What is Functional

- **Data Canvas**: Full React Flow node canvas with 1,694-line nodeRegistry (1,546+ entries), drag-and-drop, AI actions, pipeline execution engine (topological sort, LLM runner, single-node runner), 28 analytics chart types, pipeline templates, viz studio with 10 panel types
- **Notebook**: 7 feature modules + 8 cell components + 3 lib utilities + page = 24 files, ~4,146 lines. 26 features complete, 6 partial, 14 missing standard, 14 novel not started. 55% standard completion.
- **Terminal**: 28 terminal components including AI terminal, agent runner, git panel, file browser, Docker/K8s pickers, session manager, split panes, history, bookmarks, process monitor, variable explorer
- **Sidebar**: 42 sidebar panel components across root (11), canvas (15), and terminal (12) directories
- **Backend**: 13 API routers, 6 services, 6 ORM models, 6 Pydantic schemas, 30 data connectors, middleware (CORS, rate limiting, security), Alembic migrations
- **Pages**: Notebook, DataCanvas, AgentCanvas, IDE, Terminal, Chat, Connectors, VizStudio (10 route pages)
- **Shared UI**: SidebarSection + SidebarSectionStack (canonical primitives), ResizeSash
- **AI**: @ck/ai package with browser and server clients, model registry, AiActions + AiChat features

### What is Scaffolded/Empty

- **apps/agent-canvas/**: 285 files but only 2,177 total lines -- mostly generated stubs from the data-canvas scaffold. App.tsx and main.tsx exist but minimal content.
- **packages/@ck/sync/**: Single index.ts -- Yjs/CRDT real-time sync not yet implemented
- **packages/@ck/types/**: Single index.ts -- shared types still mostly live in apps/data-canvas/src/lib/types.ts and shared/
- **backend/tests/**: conftest.py + .gitkeep only -- backend test coverage minimal
- **electron-app/**: Exists but not audited for completeness
- **kernel-gateway/**: Docker compose config, not a full implementation

### What is Planned but Not Built

- Reactive execution engine (Marimo-style AST analysis)
- Branch/Compare/Replace system
- Cell contracts with auto-inference
- Agent cells as DAG nodes
- Living pipeline / continuous execution
- Cell-level RBAC
- Pyodide browser fallback execution
- Multi-kernel support (Python + R + Julia)
- Tournament cells
- Notebook-Canvas bidirectional sync
- MCP server support
- ComfyUI-style node marketplace

---

## 3. Notebook's Place in the Architecture

### Location

The notebook lives entirely within the **data-canvas** app at:
`apps/data-canvas/src/`

It spans three directories:
1. **Feature modules**: `apps/data-canvas/src/features/notebook/`
2. **Cell components**: `apps/data-canvas/src/components/cell/`
3. **Cell utilities**: `apps/data-canvas/src/lib/` (cell-operations, cell-execution, cell-history, kernel-client)
4. **Page component**: `apps/data-canvas/src/pages/NotebookPage.tsx`

### Dependencies

The notebook depends on:
- **@ck/ai** -- for AI-generated cells (BetweenCellMenu AI Generate, AiActions)
- **@ck/ui** -- SidebarSection/SidebarSectionStack used in CellListPanel
- **shared/notebook.ts** -- NotebookCell, CellOutput, NotebookDocument type definitions
- **shared/kernel.ts** -- KernelInfo, KernelExecuteRequest/Reply types
- **shared/session.ts** -- SessionInfo types
- **lib/kernel-client.ts** -- WebSocket connection to Jupyter Kernel Gateway
- **lib/event-bus.ts** -- inter-component communication
- **lib/command-registry.ts** -- command palette registration
- **stores/canvasStore.ts** -- shared canvas state (for cross-tool bridge)
- **components/editor/MonacoWrapper.tsx** -- code editor (all code/SQL/markdown cells)

### Feature Module Map

| Module | Path | Lines | Description |
|--------|------|-------|-------------|
| notebook-store | `features/notebook/notebook-store.ts` | 341 | Zustand store: cells[], activeCellId, 16 CRUD actions, undo/redo (50 snapshots), multi-select |
| notebook-execute | `features/notebook/notebook-execute.ts` | 144 | executeCell, runAndAdvance, runAndStay, runAndInsertBelow, timing |
| notebook-keyboard | `features/notebook/notebook-keyboard.ts` | 500 | 18 keyboard shortcuts (command mode + edit mode), 22 command palette commands |
| notebook-save | `features/notebook/notebook-save.ts` | 319 | localStorage auto-save (30s), Ctrl+S, server POST, dirty tracking, title |
| notebook-export | `features/notebook/notebook-export.ts` | 410 | 8 formats: .py, .ipynb (nbformat v4.5), .md, .html, .pdf, .tex, slides, .docx |
| notebook-import | `features/notebook/notebook-import.ts` | 328 | .ipynb import with output/MIME preservation, clipboard paste detection |
| notebook-modes | `features/notebook/notebook-modes.ts` | 204 | 5 modes: Normal, Focus, Zen, Presentation, Pipeline |

### Cell Component Map

| Component | Path | Lines | Description |
|-----------|------|-------|-------------|
| Cell.tsx | `components/cell/Cell.tsx` | 236 | Dispatcher: drag-and-drop, click-to-select, active border, status indicator |
| CodeCell.tsx | `components/cell/CodeCell.tsx` | 71 | Monaco editor + output, language mapping (Python/JS/SQL/HTML) |
| MarkdownCell.tsx | `components/cell/MarkdownCell.tsx` | 111 | Edit mode (Monaco) + simple preview renderer. PARTIAL -- missing full markdown/KaTeX |
| SqlCell.tsx | `components/cell/SqlCell.tsx` | 62 | Monaco SQL editor + table output |
| CellOutput.tsx | `components/cell/CellOutput.tsx` | 91 | Output dispatcher: stream, execute_result, display_data, error. 6 MIME types |
| DataFrameRenderer.tsx | `components/cell/DataFrameRenderer.tsx` | 276 | Sort, filter, paginate, column stats, CSV export, clipboard, Observatory theme |
| CellToolbar.tsx | `components/cell/CellToolbar.tsx` | 215 | Type badge, language selector, run/move/delete, more menu (10+ actions) |
| BetweenCellMenu.tsx | `components/cell/BetweenCellMenu.tsx` | 188 | Insert code/md/SQL/JS, snippet library (8 built-in), template, AI generate |
| index.ts | `components/cell/index.ts` | 10 | Barrel export |

### Cell Utility Map

| Utility | Path | Lines | Description |
|---------|------|-------|-------------|
| cell-operations.ts | `lib/cell-operations.ts` | 244 | 32 NB.* functions: CRUD, clipboard, move, merge, split, collapse, lock, find/replace |
| cell-execution.ts | `lib/cell-execution.ts` | 98 | Queue-based execution with progress tracking |
| cell-history.ts | `lib/cell-history.ts` | 29 | Per-cell version snapshots, restore |
| kernel-client.ts | `lib/kernel-client.ts` | 412 | WebSocket to Jupyter Kernel Gateway, streaming outputs, reconnect, interrupt |

### Sidebar Panel

| Panel | Path | Description |
|-------|------|-------------|
| CellListPanel.tsx | `features/sidebar/CellListPanel.tsx` | 153 lines. Cell list with type badges and preview snippets |
| VariableExplorer.tsx | `features/sidebar/VariableExplorer.tsx` | Sidebar variable explorer (exists, implementation depth TBD) |

---

## 4. Monolith Migration Status

### Monolith Source Files

| File | Lines | Size | Migration Status |
|------|-------|------|-----------------|
| data-lab.html | 15,403 | ~600KB | **55% migrated**. Cell CRUD, keyboard, save/load, export/import, modes, execution all ported. Missing: voice-to-code, Pyodide fallback, sql.js, IndexedDB, collaborative hints, variable explorer integration, inline profiling, chart recommendation |
| ck-core.1.0.js | 1,066 | ~56KB | **Partially migrated**. Core engine functions split across lib/ utilities and Zustand stores. Auth, API client, event bus ported. Shared layout/routing ported to React Router + Sidebar/Topbar/StatusBar |
| ck-data.1.0.js | 406 | ~18KB | **Partially migrated**. DataFrame operations ported to DataFrameRenderer.tsx and dataframe-utils.ts. Missing: in-browser SQLite (sql.js), Pyodide data engine, full variable explorer, inline data profiling |
| ck-editor.1.0.js | 190 | ~6KB | **Fully migrated**. Monaco editor management replaced by MonacoWrapper.tsx + CodeMirror 6 integration |
| ck-files.1.0.js | 745 | ~25KB | **Partially migrated**. File browser ported to FilesPanel.tsx sidebar + backend files router. Missing: IndexedDB workspace cache |
| ck-observe.1.0.js | 693 | ~30KB | **Partially migrated**. Observability concepts ported to AnalyticsPanel.tsx and 28 analytics chart components. Missing: full observability panel integration |
| ck-universal.js | 784 | ~30KB | **Partially migrated**. AI call layer ported to @ck/ai package + AiActions.ts + AiChat.tsx + AiActionsSection in nodes. Missing: voice-to-code (CK_Voice), text-to-speech (CK_Speak). voice-input.ts and micInput.tsx exist as stubs |

### Monolith Pages Migration

| Monolith Page | Lines | Modern Equivalent | Status |
|---------------|-------|-------------------|--------|
| data-lab.html | 15,403 | NotebookPage.tsx (251 lines) | 55% feature parity |
| data-lab-ide.html | ~3,000 est | IdePage.tsx | Ported |
| data-canvas.html | ~5,000 est | DataCanvasPage.tsx + DataCanvasFlow.tsx | Ported (primary app) |
| agent-canvas.html | ~4,000 est | AgentCanvasPage.tsx + AgentCanvasFlow.tsx | Ported (scaffolded) |
| terminal.html | ~2,000 est | TerminalPage.tsx + 28 terminal components | Ported |
| chat.html | ~1,500 est | ChatPage.tsx | Ported |
| connectors.html | ~1,000 est | ConnectorsPage.tsx + 30 backend connectors | Ported |

### What Has NOT Been Migrated

1. **Voice-to-code (CK_Voice)** -- mic button on every textarea, Web Speech API. Stubs exist (voice-input.ts, micInput.tsx, VoiceControls.tsx) but not functional.
2. **Text-to-speech (CK_Speak)** -- read cell output aloud. Not ported.
3. **Pyodide in-browser execution** -- browser-only Python via WebAssembly. Not ported.
4. **sql.js in-browser SQLite** -- client-side SQL execution. Not ported.
5. **IndexedDB workspace file cache** -- offline file access. Not ported.
6. **Collaborative editing hints** -- real-time cursor/selection sharing. @ck/sync package exists but is stub only.
7. **Cell-level execution metrics** -- per-cell performance tracking across runs. Not ported.
8. **Variable explorer integration** -- kernel variable inspection sidebar. VariableExplorer.tsx exists in both sidebar and terminal but depth of implementation unknown.
9. **Inline data profiling** -- per-DataFrame column stats/distributions. computeProfiles.ts exists in nodes/data/ but not in notebook cells.
10. **Chart recommendation engine** -- automatic chart type suggestion. chartRouting.ts exists in nodes/data/ but not notebook-integrated.

---

## 5. Dependencies and Build System

### pnpm Workspace Configuration

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/@ck/*"
  - "tooling/*"
```

Requires pnpm >= 9.0.0 and Node.js >= 20.0.0.

### Build Commands

| Command | What it does |
|---------|-------------|
| `pnpm build` | Turborepo builds all packages, then all apps |
| `pnpm dev` | Turborepo starts all dev servers in parallel |
| `pnpm dev:data-canvas` | Dev server for data-canvas only |
| `pnpm dev:suite` | Dev server for @ck/suite (if exists) |
| `pnpm build:data-canvas` | Build data-canvas only |
| `pnpm build:packages` | Build all @ck/* packages |
| `pnpm lint` | ESLint + TypeScript strict on all packages |
| `pnpm typecheck` | TypeScript type checking |
| `pnpm clean` | Remove dist/ and .turbo/ |

### Makefile Shortcuts

| Target | Command |
|--------|---------|
| `dev-frontend` | `cd frontend && npm run dev` |
| `dev-backend` | `cd backend && uvicorn app.main:app --reload --port 8000` |
| `dev-kernel` | `cd kernel-gateway && docker compose up -d` |
| `build-frontend` | `cd frontend && npm run build` |
| `build-backend` | `cd backend && docker build -t ck-backend .` |
| `test` | Runs both frontend (Vitest, 296 tests) and backend (pytest) |
| `lint` | Frontend (ESLint + typecheck) + Backend (ruff + mypy) |
| `deploy` | `powershell -File infra/deploy/deploy.ps1` |

Note: The Makefile references `frontend/` paths but the monorepo uses `apps/data-canvas/`. The Makefile may predate the monorepo restructuring.

### Dev Server Ports

| Service | Port | Description |
|---------|------|-------------|
| Data Canvas (Vite) | 5173 (default Vite) | Frontend dev server |
| FastAPI backend | 8000 | `uvicorn --port 8000` |
| Jupyter Kernel Gateway | 8888 | Python execution |

### TypeScript Configuration

Root `tsconfig.base.json`: ES2022 target, strict mode, react-jsx, bundler module resolution, declaration + declarationMap + sourceMap enabled. Each package/app extends this with its own tsconfig.json.

### Turborepo Configuration

`turbo.json` defines 6 tasks: build (cached, depends on ^build), dev (persistent, no cache), typecheck, lint, test (depends on build), clean. Global dependencies: tsconfig.base.json. Global env: NODE_ENV, CI, VITE_*.

### CI/CD (GitHub Actions)

On push/PR to main:
- Frontend: typecheck, lint, test (296 tests), build
- Backend: ruff, mypy, pytest
- Deploy: auto-deploy on merge to main via SSH to 45.79.187.74

---

## 6. Cross-Reference with Research Synthesis

### Reactive Execution (Marimo-style AST Analysis)

**Synthesis recommendation**: Static AST analysis as default (Pyodide-compatible) + typed cell contracts as escape hatch for mutation edge cases.

**Where to implement**:
- New file: `apps/data-canvas/src/features/notebook/notebook-reactive.ts` -- AST dependency graph builder, dirty-flag propagation, topological execution scheduler
- Extends: `features/notebook/notebook-execute.ts` (144 lines) -- add reactive mode alongside manual
- Depends on: `features/notebook/notebook-store.ts` -- add dependency graph to store state
- Cross-reference: `engine/topologicalSort.ts` already implements topological sort for canvas pipeline execution -- can be adapted for reactive cell execution
- Browser execution: Future Pyodide integration would use Hamilton-style function-signature-as-DAG (Pyodide-compatible per synthesis)

### Cell Types (78-Type Taxonomy)

**Synthesis recommendation**: 78 cell types across 8 tiers (Compute, Display, Input, Data, AI, Pipeline, Agent, Infrastructure).

**Current state**: 12 cell types defined in `shared/notebook.ts` (CellType = 'code' | 'markdown' | 'raw'). The full cell type literal union lives in `apps/data-canvas/src/lib/types.ts` with extended types (code, md, sql, js, viz, form, raw, scratch, latex, mermaid, html, prompt).

**Where cell type components live**:
- Existing: `apps/data-canvas/src/components/cell/` -- CodeCell, MarkdownCell, SqlCell, CellOutput, DataFrameRenderer
- Cell type dispatch: `apps/data-canvas/src/components/cell/Cell.tsx` (line ~50+) -- switch on cell.type
- To add new cell types: Create component in `components/cell/`, register in Cell.tsx dispatch, add type literal to types.ts

**How to scale to 78+ types**: Follow the same pattern as nodeRegistry.ts (1,694 lines, 1,546+ entries) but with lazy loading via dynamic `import()`. The synthesis recommends SQLite FTS5 index for search across 10K+ types and virtual scrolling for the cell type picker.

### Node Registry (10K+ Types with Lazy Loading)

**Current location**: `apps/data-canvas/src/nodes/nodeRegistry.ts` -- 1,694 lines, 1,546+ entries. DO NOT TOUCH per CLAUDE.md.

**Relationship to notebook cells**: The nodeRegistry defines Data Canvas nodes. These are distinct from notebook cell types but architecturally parallel. The synthesis envisions all 178+ Agent Canvas node types becoming available as notebook cells (per NOTEBOOK_ARCHITECTURE.md). The bridge would be:
- `apps/data-canvas/src/features/bridges/cross-tool-bridge.ts` -- existing bridge between tools
- `apps/data-canvas/src/features/canvas/node-registry.ts` -- canvas-specific node registry (separate from the main nodeRegistry.ts)
- `apps/data-canvas/src/features/canvas/node-registry.json` -- JSON node registry data

**Scaling path**: The synthesis recommends ComfyUI-style typed I/O declarations + SQLite FTS5 + lazy loading. The current registry is a single static file -- migration to lazy-loaded chunks would happen in a new `features/notebook/cell-registry.ts` without touching nodeRegistry.ts.

### Pipeline/DAG Framework

**Current execution engine**: `apps/data-canvas/src/engine/`
- `topologicalSort.ts` -- DAG topological sort (used for canvas pipeline execution)
- `pipelineRunner.ts` -- orchestrates full pipeline runs
- `singleNodeRunner.ts` -- executes individual nodes
- `llmRunner.ts` -- LLM-specific node execution
- `resultExtractor.ts` -- extracts outputs from node execution

**Synthesis recommendation**: Hamilton (Pyodide-compatible) for browser-side pipelines + Kedro Data Catalog pattern for persistence. The existing engine/ directory is the foundation. Reactive notebook execution would add:
- `features/notebook/notebook-reactive.ts` -- cell-level DAG (adapting engine/topologicalSort.ts)
- `features/notebook/notebook-contracts.ts` -- typed cell contracts (Pandera + Pydantic under the hood)
- `features/notebook/notebook-pipeline.ts` -- Hamilton integration for browser-side pipeline mode

**Node contract data already exists**: `apps/data-canvas/src/nodes/data/nodeContracts.ts` and `nodes/data/contractMeta.ts` define contract metadata for canvas nodes -- these patterns would be adapted for notebook cell contracts.

### Variable Explorer

**Current locations**:
- `apps/data-canvas/src/features/sidebar/VariableExplorer.tsx` -- sidebar variable explorer panel
- `apps/data-canvas/src/components/terminal/VariableExplorer.tsx` -- terminal variable explorer

**Synthesis recommendation**: Positron's OpenRPC protocol + Spyder's editing depth + Deepnote's inline profiling + variable lineage tracking (novel). Implementation would extend the existing VariableExplorer components with:
- OpenRPC communication layer in `lib/variable-client.ts` (new)
- Backend endpoint in `backend/app/routers/` (new router or extend notebooks.py)
- Kernel-side variable inspection via `lib/kernel-client.ts` (extend existing)

### Branch/Compare/Replace

**Where to implement**:
- `features/notebook/notebook-branch.ts` -- branch creation, parallel execution, state forking
- `features/notebook/notebook-compare.ts` -- statistical comparison engine (paired t-test, McNemar's, Wilcoxon, Diebold-Mariano)
- `features/notebook/notebook-replace.ts` -- winner promotion, approval gates
- `components/cell/BranchCell.tsx` -- branch UI indicator
- `components/cell/ComparisonCell.tsx` -- comparison results display
- `features/sidebar/canvas/ExperimentsPanel.tsx` -- already exists, could be adapted for branch experiment tracking

**Backend support**: `backend/app/routers/notebooks.py` + `backend/app/services/notebook_service.py` would need branch state persistence. The `backend/app/models/notebook.py` model would need branch/version metadata.

**Statistical testing**: Backend-side in a new `backend/app/services/statistics_service.py` using scipy/statsmodels. The existing `components/analytics/StatisticalTestsChart.tsx` provides the frontend visualization pattern.
