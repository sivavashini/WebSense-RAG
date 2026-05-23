from pydantic import BaseModel, Field
from fastapi import APIRouter, Request

from services.database import add_incident
from services.llm import generate_answer
from services.risk import actions_for, classify_risk
from services.vector_store import retrieve
from services.websocket import manager

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=6000)
    top_k: int = Field(4, ge=1, le=8)


@router.post("/chat")
async def chat(payload: ChatRequest, request: Request):
    risk = classify_risk(payload.message)
    evidence = retrieve(payload.message, payload.top_k)
    answer = generate_answer(payload.message, risk, evidence)
    actions = actions_for(risk.risk_level, risk.category)
    incident_id = add_incident(
        {
            "situation": payload.message,
            "response": answer,
            "risk_level": risk.risk_level,
            "category": risk.category,
            "confidence": risk.confidence,
            "evidence": evidence,
            "actions": actions,
        }
    )
    result = {
        "incident_id": incident_id,
        "ai_response": answer,
        "risk": {"risk_level": risk.risk_level, "category": risk.category, "confidence": risk.confidence},
        "evidence": evidence,
        "actions": actions,
    }
    await manager.broadcast({"type": "chat_complete", "risk": result["risk"]})
    return result
