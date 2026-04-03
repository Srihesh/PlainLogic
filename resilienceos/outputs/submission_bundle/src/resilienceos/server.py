from __future__ import annotations

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from .environment import ResilienceOSEnvironment
from .models import Action


class ResetRequest(BaseModel):
    task: str = "easy"
    seed: int = 7


app = FastAPI(title="resilienceos", version="0.1.0")
env = ResilienceOSEnvironment()


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/reset")
def reset(req: ResetRequest) -> dict:
    try:
        observation = env.reset(task=req.task, seed=req.seed)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"observation": observation.model_dump()}


@app.post("/step")
def step(action: Action) -> dict:
    try:
        result = env.step(action)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.model_dump()


@app.get("/state")
def state() -> dict:
    try:
        return env.state().model_dump()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
