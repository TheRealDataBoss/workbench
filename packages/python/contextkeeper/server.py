"""contextkeeper REST API server -- FastAPI backend for MCP + GPT action."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from contextkeeper import api

app = FastAPI(
    title="contextkeeper",
    description="Zero model drift between AI agents. Universal session continuity for Claude, GPT, Gemini, and any LLM.",
    version="0.2.4",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InitRequest(BaseModel):
    project: Optional[str] = None
    bridge: Optional[str] = None
    project_type: Optional[str] = None


class SyncRequest(BaseModel):
    bridge: Optional[str] = None
    dry_run: bool = False


class BootstrapRequest(BaseModel):
    project: str
    bridge: Optional[str] = None
    clipboard: bool = False


@app.post("/init")
def init_endpoint(req: InitRequest):
    """Initialize contextkeeper state files in the current project directory."""
    try:
        result = api.init(project=req.project, bridge=req.bridge, project_type=req.project_type)
        return {"success": result["success"], "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.post("/sync")
def sync_endpoint(req: SyncRequest):
    """Sync project state files to the GitHub bridge repo."""
    try:
        result = api.sync(bridge=req.bridge, dry_run=req.dry_run)
        return {"success": result["success"], "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.get("/status")
def status_endpoint(bridge: Optional[str] = None):
    """Get status of all projects tracked in the bridge repo."""
    try:
        result = api.status(bridge=bridge)
        return {"success": result["success"], "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.post("/bootstrap")
def bootstrap_endpoint(req: BootstrapRequest):
    """Generate a paste-ready bootstrap prompt for any AI chat."""
    try:
        result = api.bootstrap(project=req.project, bridge=req.bridge, clipboard=req.clipboard)
        return {"success": True, "data": {"prompt": result}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


@app.get("/doctor")
def doctor_endpoint():
    """Run the contextkeeper environment health check."""
    try:
        result = api.doctor()
        return {"success": result["success"], "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def main():
    """Entry point for contextkeeper-server command."""
    import uvicorn

    uvicorn.run("contextkeeper.server:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
