from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from services.database import list_incidents

router = APIRouter(tags=["reports"])


@router.get("/reports/{incident_id}.pdf")
async def incident_report(incident_id: int):
    incident = next((item for item in list_incidents(200) if item["id"] == incident_id), None)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    text = pdf.beginText(40, 750)
    text.textLine("WebSense RAG Incident Report")
    text.textLine(f"Incident #{incident_id}")
    text.textLine("")
    if incident:
        for line in [
            f"Created: {incident['created_at']}",
            f"Risk: {incident['risk_level']} | Category: {incident['category']} | Confidence: {incident['confidence']}",
            f"Situation: {incident['situation'][:180]}",
        ]:
            text.textLine(line)
        text.textLine("")
        for line in incident["response"].splitlines()[:32]:
            text.textLine(line[:95])
    else:
        text.textLine("Incident not found.")
    pdf.drawText(text)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=websense-report.pdf"})
