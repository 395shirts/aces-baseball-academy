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

    # 1. Create GHL contact (non-blocking - if it fails, emails still go)
    result = None
    try:
        result = await call_tool(
            source_id="highlevel_oauth__pipedream",
            tool_name="highlevel_oauth-create-contact",
            arguments={
                "name": reg.parent_name,
                "email": reg.email,
                "phone": reg.phone,
            "additionalOptions": {
                "firstName": (reg.parent_name.split(" ")[0] if reg.parent_name else ""),
                "lastName": (" ".join(reg.parent_name.split(" ")[1:]) if reg.parent_name and len(reg.parent_name.split(" ")) > 1 else ""),
                "tags": [
                    "Summer Camp 2026",
                    "Baseball Camp",
                    "Aces Baseball Academy",
                    f"Player: {player_name}",
                    f"Weeks: {len(reg.weeks)}",
                    f"Total: ${total}",
                ],
                "source": "Landing Page",
                }
            }
        )
        print(f"[GHL] Contact created for {reg.email}")
    except Exception as e:
        print(f"[GHL] Contact creation failed: {e}")

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

    # 3. Send branded confirmation email to the PARENT
    weeks_html = ""
    for w in reg.weeks:
        weeks_html += f'<tr><td style="font-family:Arial,sans-serif;font-size:14px;color:#ffffff;padding:6px 0;">✓ {w}</td></tr>'

    confirmation_html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background-color:#f2f4f8;font-family:Arial,Helvetica,sans-serif;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f2f4f8;">
<tr><td align="center" style="padding:32px 16px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.12);">

<!-- HEADER -->
<tr><td style="background-color:#0a0e1a;padding:40px 32px 32px;text-align:center;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td align="center" style="padding-bottom:18px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="background-color:#c9a84c;height:3px;width:60px;"></td><td style="width:12px;"></td>
<td style="font-size:32px;line-height:1;">&#9918;</td>
<td style="width:12px;"></td><td style="background-color:#c9a84c;height:3px;width:60px;"></td>
</tr></table></td></tr></table>
<div style="font-size:28px;font-weight:900;letter-spacing:4px;color:#c9a84c;text-transform:uppercase;line-height:1.2;">ACES BASEBALL</div>
<div style="font-size:28px;font-weight:900;letter-spacing:4px;color:#ffffff;text-transform:uppercase;line-height:1.2;margin-bottom:10px;">ACADEMY</div>
<div style="font-size:13px;color:#a8b4cc;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px;">Summer Camp 2026</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;"><tr>
<td style="background-color:#c9a84c;border-radius:4px;padding:8px 22px;">
<span style="font-size:13px;font-weight:700;color:#0a0e1a;letter-spacing:1.5px;text-transform:uppercase;">&#10003; Registration Confirmed</span>
</td></tr></table>
</td></tr>

<!-- GREETING -->
<tr><td style="padding:36px 36px 20px;">
<p style="font-size:18px;font-weight:700;color:#0a0e1a;margin:0 0 12px;">Dear {reg.parent_name},</p>
<p style="font-size:15px;color:#3a4a5c;line-height:1.7;margin:0 0 14px;">
We are thrilled to confirm that <strong style="color:#0a0e1a;">{player_name}</strong> has been registered for <strong style="color:#0a0e1a;">Aces Baseball Academy Summer Camp 2026</strong>! Get ready for an incredible summer of skill-building, teamwork, and next-level baseball training.
</p>
</td></tr>

<!-- REGISTRATION DETAILS -->
<tr><td style="padding:8px 36px 28px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#0a0e1a;border-radius:8px;overflow:hidden;">
<tr><td style="background-color:#c9a84c;padding:10px 24px;"><span style="font-size:12px;font-weight:700;color:#0a0e1a;letter-spacing:2px;text-transform:uppercase;">Your Registration</span></td></tr>
<tr><td style="padding:24px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td style="padding-bottom:14px;vertical-align:top;width:28px;"><span style="font-size:18px;">&#128197;</span></td>
<td style="padding-bottom:14px;vertical-align:top;padding-left:10px;">
<div style="font-size:11px;color:#c9a84c;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;margin-bottom:3px;">Player</div>
<div style="font-size:15px;color:#ffffff;font-weight:600;">{player_name} (Age {reg.age or "N/A"})</div>
</td></tr>
<tr><td style="padding-bottom:14px;vertical-align:top;width:28px;"><span style="font-size:18px;">&#9989;</span></td>
<td style="padding-bottom:14px;vertical-align:top;padding-left:10px;">
<div style="font-size:11px;color:#c9a84c;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;margin-bottom:6px;">Weeks Selected ({len(reg.weeks)} week{"s" if len(reg.weeks) != 1 else ""})</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0">{weeks_html}</table>
</td></tr>
<tr><td style="padding-bottom:0;vertical-align:top;width:28px;"><span style="font-size:18px;">&#128176;</span></td>
<td style="padding-bottom:0;vertical-align:top;padding-left:10px;">
<div style="font-size:11px;color:#c9a84c;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;margin-bottom:3px;">Total Due</div>
<div style="font-size:22px;color:#c9a84c;font-weight:700;">${total}</div>
<div style="font-size:12px;color:#a8b4cc;margin-top:3px;">$250/week &middot; Early Bird Price</div>
</td></tr>
</table></td></tr></table>
</td></tr>

<!-- PAYMENT NOTE -->
<tr><td style="padding:0 36px 28px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#fff8e6;border-left:4px solid #c9a84c;border-radius:0 6px 6px 0;">
<tr><td style="padding:16px 20px;"><span style="font-size:14px;color:#7a5c10;line-height:1.6;">
<strong style="color:#5a3e00;">Payment Note:</strong> Payment of <strong>${total}</strong> is due at check-in or by phone. Call us at (689) 312-9568 to arrange payment in advance.
</span></td></tr></table>
</td></tr>

<!-- CAMP INFO -->
<tr><td style="padding:0 36px 28px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f7f9fc;border-radius:8px;"><tr><td style="padding:20px 24px;">
<div style="font-size:11px;color:#c9a84c;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:12px;">Camp Info</div>
<div style="font-size:14px;color:#3a4a5c;line-height:1.8;">&#128197; June 1 - August 7, 2026<br/>&#128336; Monday - Friday, 9:00 AM - 2:00 PM<br/>&#129351; Coaches: Adrian Hernandez (Former NYY) &amp; Rickie Weeks Sr. "The Professor"</div>
</td></tr></table>
</td></tr>

<!-- WHAT TO BRING -->
<tr><td style="padding:0 36px 28px;">
<div style="font-size:11px;color:#c9a84c;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:12px;">What to Bring</div>
<div style="font-size:14px;color:#3a4a5c;line-height:1.8;">&#129351; Baseball glove &middot; &#9918; Bat (optional) &middot; &#128095; Athletic shoes &middot; &#128167; Water bottle &middot; &#9728;&#65039; Sunscreen &middot; &#127822; Snacks/lunch</div>
</td></tr>

<!-- CONTACT -->
<tr><td style="padding:10px 36px 32px;text-align:center;">
<div style="font-size:11px;color:#c9a84c;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:10px;">Questions?</div>
<div style="font-size:15px;color:#0a0e1a;font-weight:700;">&#128222; (689) 312-9568 &nbsp;&middot;&nbsp; <a href="https://acesportsacademy.net" style="color:#c9a84c;text-decoration:none;font-weight:700;">acesportsacademy.net</a></div>
</td></tr>

<!-- FOOTER -->
<tr><td style="background-color:#0a0e1a;padding:24px 36px;text-align:center;">
<div style="font-size:18px;font-weight:900;color:#c9a84c;letter-spacing:3px;text-transform:uppercase;margin-bottom:6px;">ACES BASEBALL ACADEMY</div>
<div style="font-size:12px;color:#6a7a90;margin-bottom:10px;">Summer Camp 2026</div>
<div style="border-top:1px solid #1e2540;margin-bottom:14px;"></div>
<p style="font-size:12px;color:#4a5a70;margin:0;">&copy; 2026 Aces Baseball Academy &bull; <a href="https://acesportsacademy.net" style="color:#c9a84c;text-decoration:none;">acesportsacademy.net</a></p>
</td></tr>

</table></td></tr></table>
</body></html>'''

    confirmation_plain = f"""Dear {reg.parent_name},

We are thrilled to confirm that {player_name} has been registered for Aces Baseball Academy Summer Camp 2026!

Your Registration:
- Player: {player_name} (Age {reg.age or 'N/A'})
- Weeks: {weeks_str}
- Total Due: ${total} ($250/week Early Bird)

Payment of ${total} is due at check-in or by phone: (689) 312-9568

Camp Info:
- June 1 - August 7, 2026
- Monday - Friday, 9:00 AM - 2:00 PM
- Coaches: Adrian Hernandez (Former NYY) & Rickie Weeks Sr. "The Professor"

What to Bring: Baseball glove, bat (optional), athletic shoes, water bottle, sunscreen, snacks/lunch

Questions? Call (689) 312-9568 or visit acesportsacademy.net

- Aces Baseball Academy
"""

    try:
        await call_tool(
            source_id="gcal",
            tool_name="send_email",
            arguments={
                "action": {
                    "action": "send",
                    "to": [reg.email],
                    "cc": [],
                    "bcc": ["launchgloble@gmail.com", "info@acesacademy.net"],
                    "subject": f"You're Registered! \u26be Aces Baseball Academy Summer Camp 2026",
                    "body": confirmation_plain,
                    "html_body": confirmation_html,
                }
            }
        )
        print(f"[EMAIL] Confirmation sent to {reg.email} (bcc: launchgloble, info@aces)")
    except Exception as e:
        print(f"[EMAIL] Could not send confirmation: {e}")

    return {"success": True, "contact": result}


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
