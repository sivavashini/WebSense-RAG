import google.generativeai as genai
from openai import OpenAI

from services.config import settings
from services.risk import RiskResult


SYSTEM_PROMPT = """You are WebSense AI. First understand the user's real situation.

Classify into one of:
- Pet Safety
- Lost & Found
- Public Help
- Cyber Threat
- Physical Threat
- Medical Emergency
- Ethical Concern
- Suspicious Activity
- Harassment
- Theft

Rules:
1. Do not assume every situation is dangerous.
2. For missing pets/items, give practical search steps.
3. For low-risk issues, avoid emergency wording.
4. Mention police/emergency only if injury, theft, violence, fire, or immediate danger is present.
5. Give human, situation-specific advice.
6. Never provide instructions that enable harm, crime, evasion, or cyber abuse.
7. Use retrieved context when relevant. If evidence is weak, say so clearly.

Return with these exact headings:
Situation Summary
Risk Level
Immediate Action
Best Responsible Choice
Things To Avoid
Escalation Advice
"""


def build_prompt(situation: str, risk: RiskResult, evidence: list[dict]) -> str:
    context = "\n\n".join(
        f"Source: {item['source']} chunk {item['chunk']} score {item['score']:.3f}\n{item['text']}"
        for item in evidence
    ) or "No indexed documents were available. Use general safety reasoning and say evidence is limited."
    return f"""{SYSTEM_PROMPT}

Detected classification:
Risk Level: {risk.risk_level}
Category: {risk.category}
Confidence: {risk.confidence}

Retrieved evidence:
{context}

User situation:
{situation}
"""


def fallback_answer(situation: str, risk: RiskResult) -> str:
    return local_safety_answer(risk, "No live model key is configured, so WebSense used the local safety engine.")


def local_safety_answer(risk: RiskResult, status: str | None = None) -> str:
    if risk.category == "Pet Safety":
        body = f"""Situation Summary
This sounds like a pet safety or missing pet situation. It may be stressful, but it is not automatically an emergency unless the pet or a person is in immediate danger.

Risk Level
{risk.risk_level} with {risk.confidence:.0%} confidence.

Immediate Action
Start from the last known location, call the pet by name, check hiding spots, ask nearby people, and share a clear photo with collar or microchip details.

Best Responsible Choice
Contact local shelters, nearby vets, building security, and neighborhood groups while keeping one person reachable by phone.

Things To Avoid
Avoid chasing the pet into traffic, posting your full home address publicly, or assuming someone stole the pet without evidence.

Escalation Advice
Contact animal control, shelters, or local authorities only if the animal is injured, trapped, aggressive, stolen, or creating immediate public danger."""
    elif risk.category == "Lost & Found":
        body = f"""Situation Summary
This sounds like a lost or found item situation. It may be inconvenient or concerning, but it is not automatically dangerous.

Risk Level
{risk.risk_level} with {risk.confidence:.0%} confidence.

Immediate Action
Retrace your steps, check the most likely places, and contact the venue, transport desk, building security, or lost-and-found counter.

Best Responsible Choice
If the item contains money, cards, IDs, or personal data, protect accounts and report or lock sensitive items if misuse is possible.

Things To Avoid
Avoid accusing people without evidence, sharing sensitive ID details publicly, or delaying card/account protection if the item can be misused.

Escalation Advice
Involve police only if there is clear theft, fraud, threats, or misuse of identity or property."""
    elif risk.category == "Public Help":
        body = f"""Situation Summary
This sounds like a public help situation. The goal is to assist without putting yourself or others at unnecessary risk.

Risk Level
{risk.risk_level} with {risk.confidence:.0%} confidence.

Immediate Action
Ask what help is needed from a safe distance and involve nearby staff, neighbors, or another trusted person if the situation is unclear.

Best Responsible Choice
Offer practical support while keeping boundaries, privacy, and personal safety in mind.

Things To Avoid
Avoid entering isolated places alone, sharing private information, or escalating the situation with assumptions.

Escalation Advice
Call emergency services only if someone is injured, unconscious, threatened, trapped, or in immediate danger."""
    elif risk.category == "Cyber Threat":
        body = f"""Situation Summary
This appears related to a possible cyber threat, such as phishing, credential theft, account misuse, or suspicious links.

Risk Level
{risk.risk_level} with {risk.confidence:.0%} confidence.

Immediate Action
Do not click suspicious links, share OTPs, install files, or reply with private information.

Best Responsible Choice
Verify through an official channel, change exposed passwords from a trusted device, and preserve screenshots or message headers.

Things To Avoid
Avoid forwarding suspicious links, paying demands, sharing codes, or trying to hack back.

Escalation Advice
Contact your bank, platform support, workplace security team, or cybercrime reporting channel if money, accounts, or sensitive data may be at risk."""
    else:
        body = f"""Situation Summary
You described a situation that appears related to {risk.category}. WebSense is treating it according to the actual risk signals rather than assuming danger.

Risk Level
{risk.risk_level} with {risk.confidence:.0%} confidence.

Immediate Action
Take the least risky next step, protect people first, and gather accurate details before acting.

Best Responsible Choice
Choose the response that reduces harm, respects consent and privacy, and involves the right trusted person or authority only when needed.

Things To Avoid
Avoid retaliation, public accusations without evidence, deleting important records, or escalating beyond what the situation requires.

Escalation Advice
Use police or emergency services only if there is injury, theft, violence, fire, serious harassment, or immediate danger."""
    if status:
        return f"{body}\n\nModel Status\n{status}"
    return body


def legacy_fallback_answer(situation: str, risk: RiskResult) -> str:
    return f"""Situation Summary
You described a situation that appears related to {risk.category}. I do not have a live model key configured, so this response uses the local safety engine.

Risk Level
{risk.risk_level} with {risk.confidence:.0%} confidence.

Immediate Action
Protect people first, move away from immediate danger, and contact emergency services if anyone may be harmed.

Best Responsible Choice
Document what happened, involve the right authority or trusted person, and choose the action that reduces harm while respecting law, privacy, and consent.

Things To Avoid
Do not retaliate, tamper with evidence, click suspicious links, share private credentials, or confront a dangerous person alone.

Escalation Advice
If there is imminent physical danger, fire, serious injury, self-harm risk, or an active crime, call local emergency services now."""


def provider_fallback_answer(situation: str, risk: RiskResult, error_name: str) -> str:
    return local_safety_answer(
        risk,
        f"Live AI provider failed, so WebSense used the local safety fallback. Backend detail: {error_name}.",
    )


def generate_answer(situation: str, risk: RiskResult, evidence: list[dict]) -> str:
    prompt = build_prompt(situation, risk, evidence)
    try:
        if settings.llm_provider.lower() == "gemini" and settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            model = genai.GenerativeModel(settings.gemini_model)
            return model.generate_content(prompt).text or fallback_answer(situation, risk)
        if settings.openai_api_key:
            client = OpenAI(api_key=settings.openai_api_key)
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                temperature=0.25,
            )
            return res.choices[0].message.content or fallback_answer(situation, risk)
    except Exception as exc:
        return provider_fallback_answer(situation, risk, type(exc).__name__)
    return fallback_answer(situation, risk)
