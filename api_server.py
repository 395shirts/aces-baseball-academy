#!/usr/bin/env python3
"""
Aces Baseball Academy — Registration API
Receives form submissions and creates contacts in GoHighLevel.
"""
import asyncio
import json
import subprocess
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class Registration(BaseModel):
    player_first: str
    player_last: str
    dob: Optional[str] = None
    age: Optional[str] = None
    skill_level: Optional[str] = None
    position: Optional[str] = None
    parent_name: str
    relationship: Optional[str] = None
    email: str
    phone: str
    emergency_name: Optional[str] = None
    emergency_phone: Optional[str] = None
    weeks: List[str] = []
    medical: Optional[str] = None


async def call_tool(source_id: str, tool_name: str, arguments: dict):
    payload = json.dumps({"source_id": source_id, "tool_name": tool_name, "arguments": arguments})
    proc = await asyncio.create_subprocess_exec(
        "external-tool", "call", payload,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(stderr.decode())
    return json.loads(stdout.decode())


@app.post("/api/register")
async def register(reg: Registration):
    player_name = f"{reg.player_first} {reg.player_last}"
    weeks_str = ", ".join(reg.weeks) if reg.weeks else "Not selected"
    total = len(reg.weeks) * 250

    # Build notes with all registration details
    notes = f"""
=== ACES BASEBALL ACADEMY — SUMMER CAMP 2026 ===

PLAYER INFO
-----------
Player Name: {player_name}
Date of Birth: {reg.dob or 'N/A'}
Age: {reg.age or 'N/A'}
Skill Level: {reg.skill_level or 'N/A'}
Position: {reg.position or 'N/A'}

PARENT / GUARDIAN
-----------------
Name: {reg.parent_name} ({reg.relationship or 'Parent'})
Email: {reg.email}
Phone: {reg.phone}
Emergency Contact: {reg.emergency_name or 'N/A'} — {reg.emergency_phone or 'N/A'}

CAMP REGISTRATION
-----------------
Weeks Selected: {weeks_str}
Total Due: ${total}
Camp Dates: June 1 – Aug 7, 2026 (Mon–Fri, 9AM–2PM)
Early Bird: $250/week

MEDICAL / NOTES
---------------
{reg.medical or 'None'}
""".strip()

    # 1. Create GHL contact
    result = await call_tool(
        source_id="highlevel_oauth__pipedream",
        tool_name="highlevel_oauth-create-contact",
        arguments={
            "name": reg.parent_name,
            "email": reg.email,
            "phone": reg.phone,
            "additionalOptions": {
                "tags": ["Summer Camp 2026", "Baseball Camp", "Aces Baseball Academy"],
                "customField": {
                    "player_name": player_name,
                    "weeks_registered": weeks_str,
                    "total_due": f"${total}",
                },
                "source": "Landing Page",
                "notes": notes,
            }
        }
    )

    # 2. Send email notifications to both addresses
    email_subject = f"New Camp Registration: {player_name} — {len(reg.weeks)} week(s) / ${total}"
    email_body = f"""New registration received from the Aces Baseball Academy landing page.

{'='*60}
PLAYER: {player_name}
AGE: {reg.age or 'N/A'} | DOB: {reg.dob or 'N/A'}
SKILL LEVEL: {reg.skill_level or 'N/A'}
POSITION: {reg.position or 'N/A'}
{'='*60}
PARENT/GUARDIAN: {reg.parent_name} ({reg.relationship or 'Parent'})
EMAIL: {reg.email}
PHONE: {reg.phone}
EMERGENCY: {reg.emergency_name or 'N/A'} — {reg.emergency_phone or 'N/A'}
{'='*60}
WEEKS SELECTED: {weeks_str}
TOTAL DUE: ${total}
{'='*60}
MEDICAL/NOTES: {reg.medical or 'None'}
{'='*60}

This contact has been added to GoHighLevel with tags:
Summer Camp 2026, Baseball Camp, Aces Baseball Academy

— Aces Baseball Academy Registration System
"""

    notify_emails = ["launchgloble@gmail.com", "info@acesacademy.net"]
    for addr in notify_emails:
        try:
            await call_tool(
                source_id="gcal",
                tool_name="send_email",
                arguments={
                    "to": addr,
                    "subject": email_subject,
                    "body": email_body,
                }
            )
        except Exception as e:
            print(f"[EMAIL] Could not send to {addr}: {e}")

    return {"success": True, "contact": result}


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
