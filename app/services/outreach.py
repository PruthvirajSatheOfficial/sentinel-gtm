from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models.gtm_models import Account as AccountModel, OutreachBrief as OutreachBriefModel

load_dotenv()
client = genai.Client()


def generate_outreach_brief(account: AccountModel) -> OutreachBriefModel:
    intents = account.buying_intents
    intent_text = (
        ", ".join([i.intent_category for i in intents if i.intent_category])
        if intents
        else "General Market Research"
    )

    system_instruction = (
        "You are a concise B2B GTM sales strategist. Write actionable, personalized "
        "outreach briefs for account executives based on target account details and "
        "buying intent signals. Keep it clear, structured, and grounded in the given data."
    )

    prompt = f"""Write a concise outreach brief for this account:

- Account Name: {account.name}
- Domain: {account.domain or "N/A"}
- Industry: {account.industry or "N/A"}
- Buying Intents: {intent_text}

Include:
1. Why reach out now (tied to the buying intents)
2. Key angle / value proposition
3. 2-3 short discovery questions or talking points
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        ),
    )

    brief_text = (response.text or "").strip() or "Outreach brief could not be generated."

    return OutreachBriefModel(
        account_id=account.id,
        brief_content=brief_text,
    )