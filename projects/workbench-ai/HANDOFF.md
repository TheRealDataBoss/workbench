# workbench-ai — Project Handoff

## What This Is
A universal AI session continuity CLI tool published on both npm and PyPI.
Users install once, run `workbench init` in any project, and get persistent
AI memory across sessions and models (Claude, GPT, Gemini).

## Current State
- **npm:** https://www.npmjs.com/package/workbench-ai (v0.1.0 LIVE)
- **PyPI:** https://pypi.org/project/workbench-ai/0.1.0/ (v0.1.0 LIVE)
- **Repo:** https://github.com/TheRealDataBoss/workbench
- **Local:** C:\Users\Steven\workbench\packages\

## Architecture
```
packages/
├── npm/
│   ├── package.json
│   ├── bin/workbench.js          ← CLI entry point
│   └── lib/
│       ├── init.js               ← workbench init
│       ├── sync.js               ← workbench sync
│       ├── status.js             ← workbench status
│       └── bootstrap.js          ← workbench bootstrap (STUB)
└── python/
    ├── pyproject.toml
    └── workbench_ai/
        ├── cli.py                ← CLI entry point
        ├── init.py
        ├── sync.py
        ├── status.py
        └── bootstrap.py          ← workbench bootstrap (STUB)
```

## Known Issues (Must Fix Before v0.2.0)
1. enquirer ESM crash — `workbench init` fails on Node 18+ due to ESM/CJS mismatch
2. sync auth broken — no PAT token flow, raw git errors for new users
3. bootstrap command missing — highest value feature, not implemented
4. neither package end-to-end tested from clean install
5. GitHub Action untested in real workflow
6. install.sh / install.ps1 untested
7. No config storage (~/.workbenchrc or equivalent)
8. No error handling UX — raw stack traces exposed to users

## Phase 1.5 — Harden Before Marketing (CURRENT)
Fix all blocking issues. Make the CLI actually work end-to-end.

## Phase 2 — Market Ready
README rewrite, quickstart GIF, workbench doctor, landing page.

## Key Decisions
- enquirer → replace with @inquirer/prompts (ESM native)
- PAT flow → store in ~/.workbenchrc (gitignored)
- bootstrap → outputs formatted copy-paste prompt block to stdout
- Python CLI must be functionally identical to npm CLI

## Environment
- Dev machine: Windows, PowerShell only
- Node: 18+, Python: 3.13
- Publish: npm publish from packages/npm/, twine from packages/python/
- GitHub: TheRealDataBoss/workbench (public repo)
