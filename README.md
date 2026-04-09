# Aces Baseball Academy — Summer Camp 2026

Landing page and registration system for the Aces Baseball Academy Youth Summer Baseball Camp.

## Features

- **Landing page** with hero, coaches section, training program details, camp info, and registration form
- **Registration backend** (FastAPI) that creates contacts in GoHighLevel CRM
- **Week selector** — parents pick individual weeks (June 1 – Aug 7) at $250/week with a live total
- **GHL integration** — every registration creates a contact with tags, player details, and selected weeks in notes

## Coaches

- **Adrian Hernandez** — Former New York Yankees Pitcher, "El Duquecito"
- **Rickie Weeks Sr.** — "The Professor", father of two MLB 1st round draft picks (Rickie Weeks Jr. #2 pick 2003, Jemile Weeks #12 pick 2008)

## Camp Details

- **Dates:** June 1 – August 7, 2026
- **Schedule:** Monday – Friday, 9:00 AM – 2:00 PM
- **Ages:** 7–14
- **Price:** $250/week (Early Bird)
- **Phone:** (689) 312-9568
- **Website:** acesportsacademy.net

## Training Program

1. Advanced Hitting Drills
2. Physical Conditioning
3. Dynamic Circuit Training
4. Fielding & Footwork
5. Throwing Mechanics
6. Reaction Time Training

## Tech Stack

- **Frontend:** Static HTML/CSS/JS (vanilla, no framework)
- **Backend:** Python FastAPI + Uvicorn
- **CRM:** GoHighLevel (OAuth) — contacts created via API
- **Fonts:** Bebas Neue, Oswald, Inter (Google Fonts)

## Project Structure

```
aces-site/
├── index.html          # Landing page + registration form
├── api_server.py       # FastAPI backend (GHL integration)
├── images/
│   ├── adrian-promo.jpg
│   ├── adrian-action.jpg
│   └── adrian-standing.jpg
└── README.md
```

## GHL Contact Fields

When a registration is submitted, the backend creates a GHL contact with:

- **Name:** Parent/guardian name
- **Email & Phone:** From the form
- **Tags:** `Summer Camp 2026`, `Baseball Camp`, `Aces Baseball Academy`
- **Source:** `Landing Page`
- **Notes:** Full registration details (player name, age, DOB, skill level, position, selected weeks, total due, emergency contact, medical info)

## Running Locally

```bash
# Start the backend
pip install fastapi uvicorn
python api_server.py

# The frontend is static — open index.html or serve with:
npx serve . -l 3000
```
