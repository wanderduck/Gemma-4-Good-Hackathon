"""Generate synthetic training data for Navigator fine-tuning.

Produces ~2500 examples across three categories:
  1. Situation extraction (~500) — user situation → structured JSON profile
  2. Plain language generation (~1500) — eligibility results → plain language response
  3. Benefits Q&A (~500) — follow-up questions about specific programs

Uses real program data from data/programs/*.json and county data as ground truth.
All generated examples use real eligibility thresholds, benefit amounts, and URLs.

Usage:
    PYTHONPATH=src uv run python scripts/generate_training_data.py
    PYTHONPATH=src uv run python scripts/generate_training_data.py --output data/training/generated.jsonl
"""

import argparse
import json
import os
import random
import sys
from pathlib import Path

# Ensure reproducibility
random.seed(42)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROGRAMS_DIR = DATA_DIR / "programs"
COUNTY_DIR = DATA_DIR / "raw" / "county_pages"
OUTPUT_DEFAULT = DATA_DIR / "training" / "generated.jsonl"


# ---------------------------------------------------------------------------
# Load real program data
# ---------------------------------------------------------------------------

def load_programs() -> list[dict]:
    programs = []
    for f in sorted(PROGRAMS_DIR.glob("*.json")):
        with open(f) as fh:
            programs.append(json.load(fh))
    return programs


def load_county_programs() -> dict[str, list[dict]]:
    counties = {}
    for county_dir in sorted(COUNTY_DIR.iterdir()):
        pf = county_dir / "programs.json"
        if pf.exists():
            with open(pf) as fh:
                data = json.load(fh)
            if isinstance(data, list):
                counties[county_dir.name] = data
    return counties


# ---------------------------------------------------------------------------
# Persona building blocks — combinatorial variety
# ---------------------------------------------------------------------------

COUNTIES = ["Hennepin", "Ramsey", "Dakota", "Scott", "Carver"]
COUNTY_CITIES = {
    "Hennepin": ["Minneapolis", "Brooklyn Park", "Plymouth", "Bloomington", "Eden Prairie"],
    "Ramsey": ["Saint Paul", "Maplewood", "Roseville", "White Bear Lake"],
    "Dakota": ["Burnsville", "Eagan", "Apple Valley", "Lakeville", "Farmington"],
    "Scott": ["Shakopee", "Prior Lake", "Savage", "Jordan"],
    "Carver": ["Chaska", "Chanhassen", "Waconia", "Norwood Young America"],
}

EMPLOYMENT_STATUSES = [
    "employed", "recently_unemployed", "long_term_unemployed",
    "self_employed", "retired", "disabled", "student",
]

HOUSEHOLD_TEMPLATES = [
    # (description_template, household_size, dependents, age_range)
    ("single, no kids", 1, [], (22, 60)),
    ("single parent with {n} kid(s)", None, None, (22, 45)),  # dynamic
    ("married couple, no kids", 2, [], (25, 65)),
    ("married couple with {n} kid(s)", None, None, (25, 50)),  # dynamic
    ("single senior", 1, [], (62, 85)),
    ("senior couple", 2, [], (62, 85)),
    ("single parent with elderly parent", None, None, (35, 55)),  # dynamic
]

INCOME_RANGES_MONTHLY = [
    (0, 0),            # no income
    (500, 1200),       # very low
    (1200, 2000),      # low
    (2000, 3000),      # moderate low
    (3000, 4500),      # moderate
    (4500, 6500),      # above moderate
    (6500, 9000),      # higher income (usually ineligible)
]

CONCERNS = ["food", "housing", "health", "childcare", "employment", "energy", "cash", "emergency"]

LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("hmn", "Hmong"),
    ("so", "Somali"),
]

READING_LEVELS = ["simple", "standard", "detailed"]

CITIZENSHIP_STATUSES = [
    ("citizen", 0.70),
    ("permanent_resident", 0.15),
    ("refugee", 0.08),
    ("undocumented", 0.05),
    ("other", 0.02),
]

VETERAN_RATE = 0.08
DISABILITY_RATE = 0.12

# Situation description templates — varied phrasing
SITUATION_TEMPLATES = [
    "I'm {age} years old, {employment_desc}. I live in {location}. {household_desc}. {income_desc}. {concern_desc}",
    "Hi, I'm a {age}-year-old {employment_desc} in {location}. {household_desc}. {income_desc}. {extra}",
    "I need help. {employment_desc}. {household_desc} and we're in {location}. {income_desc}. {concern_desc}",
    "{household_desc}. I'm {age}, living in {location}. {employment_desc}. {income_desc}. Can you help?",
    "My name is {name}. I'm {age} and I live in {location}. {employment_desc}. {household_desc}. {income_desc}. {concern_desc}",
    "We're a family of {hh_size} in {location}. {employment_desc}. {income_desc}. {concern_desc}",
    "{employment_desc} and I'm struggling. {household_desc}. We live in {location}. {income_desc}. What help is available?",
    "I'm {age}, {employment_desc}. {household_desc}. {location}. {income_desc}. I'm worried about {worry_list}.",
    "Hello, {household_desc}. I'm {employment_desc} and live in {location}. {income_desc}. {extra}",
    "I was told to check here for help. {employment_desc}. {household_desc}. {income_desc}. I live in {location}.",
]

FIRST_NAMES = [
    "Maria", "James", "Fatima", "Paj", "Mohamed", "Sarah", "David", "Ana",
    "Yia", "Abdi", "Jennifer", "Carlos", "Nkauj", "Hassan", "Lisa", "Juan",
    "Kou", "Amina", "Robert", "Rosa", "Tou", "Fartun", "Michael", "Guadalupe",
]

EMPLOYMENT_DESCRIPTIONS = {
    "employed": [
        "I work full-time making ${income}/month",
        "I have a job but it's part-time, about ${income}/month",
        "I'm currently employed, earning about ${income} a month",
        "I work as a {job} making ${income}/month",
    ],
    "recently_unemployed": [
        "I just lost my job {time_ago}",
        "I was laid off {time_ago} and I'm looking for work",
        "I got let go from my job {time_ago}",
        "I was recently fired and have no income right now",
    ],
    "long_term_unemployed": [
        "I haven't been able to find work for over a year",
        "I've been unemployed for a long time",
        "I can't find a job and it's been months",
    ],
    "self_employed": [
        "I do gig work and my income varies — some months ${income}, others much less",
        "I'm self-employed, making roughly ${income}/month but it's inconsistent",
        "I drive for rideshare apps and make about ${income} a month",
    ],
    "retired": [
        "I'm retired on Social Security, getting about ${income}/month",
        "I retired recently and my only income is ${income}/month from SS",
    ],
    "disabled": [
        "I'm on disability, getting ${income}/month from SSDI",
        "I have a disability and receive ${income}/month in benefits",
        "I can't work due to my disability. I get ${income}/month",
    ],
    "student": [
        "I'm a full-time student with limited income — about ${income}/month from my part-time job",
        "I'm going to school and only work part-time, making ${income}/month",
    ],
}

JOBS = [
    "cashier", "warehouse worker", "home health aide", "janitor",
    "food service worker", "retail associate", "daycare worker",
    "factory worker", "security guard", "delivery driver",
]

TIME_AGO = ["last week", "two weeks ago", "a month ago", "last month", "a few weeks ago"]

EXTRA_DETAILS = [
    "I'm really stressed about paying rent.",
    "My kids need health insurance.",
    "I don't have a car right now.",
    "I'm worried about feeding my family.",
    "My heating bill is really high and I can't keep up.",
    "I need childcare so I can look for a job.",
    "I have some medical bills piling up.",
    "We might get evicted soon.",
    "I'm pregnant and due in {months} months.",
    "My husband/wife just left and I'm on my own now.",
    "I was in a domestic violence situation and just left.",
    "I don't speak much English — my {language} is better.",
    "I just moved to Minnesota from another state.",
    "",  # sometimes no extra detail
]


# ---------------------------------------------------------------------------
# Persona generator
# ---------------------------------------------------------------------------

def generate_persona() -> dict:
    """Generate a random but coherent persona."""
    county = random.choice(COUNTIES)
    use_city = random.random() < 0.4
    location = random.choice(COUNTY_CITIES[county]) if use_city else f"{county} County"

    employment = random.choice(EMPLOYMENT_STATUSES)
    age = random.randint(18, 80)

    # Household
    template_idx = random.randint(0, len(HOUSEHOLD_TEMPLATES) - 1)
    ht = HOUSEHOLD_TEMPLATES[template_idx]

    if "kid" in ht[0]:
        n_kids = random.randint(1, 4)
        household_size = (1 if "single" in ht[0] else 2) + n_kids
        dependents = [{"age": random.randint(0, 17), "relationship": "child"} for _ in range(n_kids)]
        household_desc = ht[0].replace("{n}", str(n_kids))
        if n_kids == 1:
            household_desc = household_desc.replace("kid(s)", "kid")
        else:
            household_desc = household_desc.replace("kid(s)", "kids")
        age = random.randint(ht[3][0], ht[3][1])
    elif "elderly parent" in ht[0]:
        household_size = random.randint(2, 4)
        dependents = [{"age": random.randint(70, 90), "relationship": "parent"}]
        n_kids = household_size - 2
        if n_kids > 0:
            dependents += [{"age": random.randint(2, 16), "relationship": "child"} for _ in range(n_kids)]
        household_desc = f"single parent with {n_kids} kid(s) and my elderly mother" if n_kids > 0 else "living with my elderly mother"
        age = random.randint(ht[3][0], ht[3][1])
    else:
        household_size = ht[1]
        dependents = ht[2]
        household_desc = ht[0]
        age = random.randint(ht[3][0], ht[3][1])

    # Adjust age for seniors/students
    if employment == "retired":
        age = max(age, 62)
    elif employment == "student":
        age = random.randint(18, 30)

    # Income
    if employment == "recently_unemployed":
        income_monthly = random.choice([0, 0, 0, random.randint(200, 800)])
    elif employment == "long_term_unemployed":
        income_monthly = 0
    else:
        low, high = random.choice(INCOME_RANGES_MONTHLY)
        income_monthly = random.randint(low, high) if high > 0 else 0

    # Concerns — pick 1-4
    n_concerns = random.randint(1, 4)
    concerns = random.sample(CONCERNS, n_concerns)

    # Demographics
    citizenship = random.choices(
        [c[0] for c in CITIZENSHIP_STATUSES],
        weights=[c[1] for c in CITIZENSHIP_STATUSES],
    )[0]
    is_veteran = random.random() < VETERAN_RATE
    is_disabled = employment == "disabled" or random.random() < DISABILITY_RATE

    # Language
    lang_code, lang_name = random.choices(LANGUAGES, weights=[0.75, 0.12, 0.05, 0.08])[0]

    return {
        "county": county,
        "location": location,
        "age": age,
        "employment_status": employment,
        "household_size": household_size,
        "household_desc": household_desc,
        "dependents": dependents,
        "income_monthly": income_monthly,
        "concerns": concerns,
        "citizenship_status": citizenship,
        "is_veteran": is_veteran,
        "is_disabled": is_disabled,
        "language": lang_code,
        "language_name": lang_name,
        "name": random.choice(FIRST_NAMES),
    }


def persona_to_situation(persona: dict) -> str:
    """Convert a persona dict into a natural language situation description."""
    template = random.choice(SITUATION_TEMPLATES)

    income = persona["income_monthly"]
    employment = persona["employment_status"]

    # Employment description
    emp_templates = EMPLOYMENT_DESCRIPTIONS.get(employment, ["I'm {employment}"])
    emp_desc = random.choice(emp_templates)
    emp_desc = emp_desc.replace("${income}", f"{income:,}")
    emp_desc = emp_desc.replace("{job}", random.choice(JOBS))
    emp_desc = emp_desc.replace("{time_ago}", random.choice(TIME_AGO))
    emp_desc = emp_desc.replace("{employment}", employment.replace("_", " "))

    # Income description
    if income == 0:
        income_desc = random.choice([
            "I have no income right now",
            "We have no money coming in",
            "I'm not earning anything",
            "Zero income",
        ])
    else:
        income_desc = random.choice([
            f"Our household income is about ${income:,}/month",
            f"We make around ${income:,} a month total",
            f"I bring in about ${income:,} monthly",
            f"My income is ${income:,}/month",
        ])

    # Concern description
    concern_map = {
        "food": "putting food on the table",
        "housing": "keeping a roof over our heads",
        "health": "healthcare and medical bills",
        "childcare": "finding affordable childcare",
        "employment": "finding a job",
        "energy": "paying utility bills",
        "cash": "making ends meet",
        "emergency": "an emergency situation",
    }
    worry_items = [concern_map.get(c, c) for c in persona["concerns"]]
    concern_desc = f"I need help with {', '.join(worry_items)}."
    worry_list = " and ".join(worry_items[:2])

    # Extra details
    extra = random.choice(EXTRA_DETAILS)
    extra = extra.replace("{months}", str(random.randint(2, 8)))
    extra = extra.replace("{language}", persona["language_name"])

    try:
        text = template.format(
            age=persona["age"],
            employment_desc=emp_desc,
            location=persona["location"],
            household_desc=persona["household_desc"],
            income_desc=income_desc,
            concern_desc=concern_desc,
            hh_size=persona["household_size"],
            name=persona["name"],
            worry_list=worry_list,
            extra=extra,
        )
    except KeyError:
        # Fallback for templates that don't use all fields
        text = (
            f"I'm {persona['age']} years old, {emp_desc}. "
            f"I live in {persona['location']}. {persona['household_desc']}. "
            f"{income_desc}. {concern_desc}"
        )

    return text.strip()


def persona_to_profile_json(persona: dict) -> dict:
    """Convert persona to the structured JSON the intake stage should produce."""
    return {
        "income": persona["income_monthly"] * 12 if persona["income_monthly"] > 0 else None,
        "household_size": persona["household_size"],
        "county": persona["county"],
        "employment_status": persona["employment_status"],
        "dependents": persona["dependents"],
        "age": persona["age"],
        "is_veteran": persona["is_veteran"],
        "is_disabled": persona["is_disabled"],
        "citizenship_status": persona["citizenship_status"],
        "concerns": persona["concerns"],
        "language": persona["language"],
        "missing_info": [],
    }


# ---------------------------------------------------------------------------
# Determine realistic eligibility based on program rules
# ---------------------------------------------------------------------------

# FPL 2026 monthly thresholds (approximate)
FPL_2026_MONTHLY = {
    1: 1_303, 2: 1_753, 3: 2_203, 4: 2_653,
    5: 3_103, 6: 3_553, 7: 4_003, 8: 4_453,
}

def get_fpl(household_size: int, percent: int = 100) -> int:
    size = min(household_size, 8)
    base = FPL_2026_MONTHLY.get(size, FPL_2026_MONTHLY[8])
    if household_size > 8:
        base += (household_size - 8) * 450
    return int(base * percent / 100)


def check_eligibility(persona: dict, programs: list[dict]) -> list[dict]:
    """Determine which programs a persona may be eligible for."""
    results = []
    income = persona["income_monthly"]
    hh = persona["household_size"]
    has_kids = any(d["relationship"] == "child" for d in persona.get("dependents", []))
    kid_ages = [d["age"] for d in persona.get("dependents", []) if d["relationship"] == "child"]

    for prog in programs:
        pid = prog["id"]
        eligible = False
        confidence = "medium"
        reason = ""

        if pid == "snap":
            # BBCE: 200% FPL gross income
            threshold = get_fpl(hh, 200)
            if income <= threshold:
                eligible = True
                confidence = "high"
                reason = f"Household income ${income:,}/mo is below the 200% FPL limit of ${threshold:,}/mo for a household of {hh}"
            else:
                reason = f"Income ${income:,}/mo exceeds the 200% FPL limit of ${threshold:,}/mo"

        elif pid == "mfip":
            # Requires dependent child, ~130% FPL entry
            threshold = get_fpl(hh, 130)
            if has_kids and income <= threshold:
                eligible = True
                confidence = "high"
                reason = f"Has dependent child(ren) and income ${income:,}/mo is below ~130% FPL (${threshold:,}/mo)"
            elif not has_kids:
                reason = "MFIP requires a dependent child under 18"
            else:
                reason = f"Income ${income:,}/mo exceeds ~130% FPL (${threshold:,}/mo)"

        elif pid == "ccap":
            # Child Care Assistance — needs kids under 13, working/in school, income threshold
            young_kids = [a for a in kid_ages if a < 13]
            threshold = get_fpl(hh, 185)
            emp_ok = persona["employment_status"] in ("employed", "self_employed", "student", "recently_unemployed")
            if young_kids and emp_ok and income <= threshold:
                eligible = True
                confidence = "high" if income < threshold * 0.8 else "medium"
                reason = f"Has child(ren) under 13, is working/in school, income ${income:,}/mo below 185% FPL (${threshold:,}/mo)"
            elif not young_kids:
                reason = "CCAP requires children under 13"
            elif not emp_ok:
                reason = "CCAP requires employment, job search, or education activity"
            else:
                reason = f"Income ${income:,}/mo exceeds 185% FPL (${threshold:,}/mo)"

        elif pid == "wic":
            young_kids = [a for a in kid_ages if a <= 5]
            threshold = get_fpl(hh, 185)
            if (young_kids or persona["age"] < 1) and income <= threshold:
                eligible = True
                confidence = "high"
                reason = f"Has child(ren) under 5 and income below 185% FPL"
            elif not young_kids:
                reason = "WIC requires children under 5, pregnant, or postpartum"
            else:
                reason = f"Income exceeds 185% FPL"

        elif pid == "medical_assistance":
            threshold = get_fpl(hh, 138)
            if income <= threshold:
                eligible = True
                confidence = "high"
                reason = f"Income ${income:,}/mo is below 138% FPL (${threshold:,}/mo) for Medical Assistance"

        elif pid == "minnesotacare":
            ma_threshold = get_fpl(hh, 138)
            mc_threshold = get_fpl(hh, 200)
            if ma_threshold < income <= mc_threshold:
                eligible = True
                confidence = "high"
                reason = f"Income ${income:,}/mo is between 138% and 200% FPL — above MA but below MinnesotaCare limit"
            elif income <= ma_threshold:
                reason = "Would likely qualify for Medical Assistance instead (lower income)"
            else:
                reason = f"Income exceeds 200% FPL (${mc_threshold:,}/mo)"

        elif pid == "energy_assistance":
            threshold = get_fpl(hh, 200)
            if income <= threshold:
                eligible = True
                confidence = "high" if "energy" in persona["concerns"] else "medium"
                reason = f"Income below 200% FPL; may receive help with heating/cooling costs"

        elif pid == "emergency_assistance":
            if income <= get_fpl(hh, 200) and "emergency" in persona["concerns"]:
                eligible = True
                confidence = "medium"
                reason = "Facing an emergency situation with income below 200% FPL"
            elif income <= get_fpl(hh, 200):
                eligible = True
                confidence = "low"
                reason = "Income below threshold; EA available if facing housing/utility emergency"

        elif pid == "ega":
            if persona["employment_status"] in ("employed", "self_employed") and income <= get_fpl(hh, 200):
                eligible = True
                confidence = "medium"
                reason = "Working but low income; may be eligible for employment-related assistance"

        elif pid == "unemployment_insurance":
            if persona["employment_status"] == "recently_unemployed":
                eligible = True
                confidence = "high"
                reason = "Recently lost employment — may be eligible for UI benefits"
            elif persona["employment_status"] == "long_term_unemployed":
                eligible = True
                confidence = "low"
                reason = "Unemployed long-term — may be eligible if within benefit period"

        if eligible:
            results.append({
                "program": prog["name"],
                "program_id": pid,
                "confidence": confidence,
                "priority": "high" if confidence == "high" and pid in ("snap", "mfip", "medical_assistance") else "normal",
                "reason": reason,
                "benefit_amounts": prog.get("benefit_amounts", ""),
                "documents_required": prog.get("documents_required", ""),
                "application_url": prog.get("application_url", ""),
            })

    return results


# ---------------------------------------------------------------------------
# Category 1: Situation Extraction examples
# ---------------------------------------------------------------------------

INTAKE_SYSTEM = (
    "You are a benefits intake assistant. Your job is to extract structured information "
    "from a person's description of their situation.\n\n"
    "Extract the following fields into a JSON object:\n"
    "- income: annual household income (number or null)\n"
    "- household_size: total number of people in household (integer)\n"
    "- county: county name (string or null)\n"
    "- employment_status: one of \"employed\", \"recently_unemployed\", "
    "\"long_term_unemployed\", \"self_employed\", \"retired\", \"disabled\", \"student\", or null\n"
    "- dependents: list of objects with \"age\" (integer) and \"relationship\" (string)\n"
    "- age: the person's age (integer or null)\n"
    "- is_veteran: boolean (default false)\n"
    "- is_disabled: boolean (default false)\n"
    "- citizenship_status: \"citizen\", \"permanent_resident\", \"refugee\", "
    "\"undocumented\", or \"other\" (default \"citizen\")\n"
    "- concerns: list of keywords from: \"food\", \"housing\", \"health\", "
    "\"childcare\", \"employment\", \"energy\", \"cash\", \"emergency\"\n"
    "- language: detected language code (en, es, hmn, so, kar)\n"
    "- missing_info: list of critical fields still needed (empty if all present)\n\n"
    "If information is not stated, set it to null (not a guess).\n"
    "Respond ONLY with valid JSON. No explanation."
)


def generate_extraction_example(persona: dict) -> dict:
    """Generate an intake extraction training example."""
    situation = persona_to_situation(persona)
    profile = persona_to_profile_json(persona)

    # Simulate partial info — sometimes users don't provide everything
    if random.random() < 0.15:
        # Remove income from situation text and profile
        profile["income"] = None
        profile["missing_info"] = ["income"]
    if random.random() < 0.10:
        profile["missing_info"] = profile.get("missing_info", []) + ["county"]

    return {
        "messages": [
            {"role": "system", "content": INTAKE_SYSTEM},
            {"role": "user", "content": situation},
            {"role": "assistant", "content": json.dumps(profile, indent=2)},
        ]
    }


# ---------------------------------------------------------------------------
# Category 2: Plain Language Response Generation
# ---------------------------------------------------------------------------

RESPONSE_DISCLAIMER = (
    "\n\n---\n*This is an informational tool, not legal advice. "
    "Eligibility determinations are unofficial estimates. "
    "Always verify with the relevant agency before applying. "
    "Program rules change — information last verified April 2026.*"
)


def format_response(persona: dict, eligible_programs: list[dict], reading_level: str) -> str:
    """Generate a plain-language response from eligibility results."""
    if not eligible_programs:
        return (
            f"I understand you're going through a tough time. Based on what you've shared, "
            f"I wasn't able to identify specific programs that match your situation right now, "
            f"but that doesn't mean help isn't available.\n\n"
            f"I'd suggest contacting your county human services office directly — they can "
            f"do a comprehensive screening and may know of local resources I don't have "
            f"information about.\n\n"
            f"**{persona['county']} County Human Services**: You can reach them through "
            f"MNbenefits.mn.gov or by calling 211."
            + RESPONSE_DISCLAIMER
        )

    high_priority = [p for p in eligible_programs if p["priority"] == "high"]
    normal_priority = [p for p in eligible_programs if p["priority"] != "high"]

    lines = []

    # Empathetic opener
    openers = [
        "I hear you, and I want to help you find the support that's available.",
        "Thank you for sharing your situation. Let me walk you through what may be available to you.",
        "I understand things are difficult right now. Here's what I found that could help.",
        "Based on what you've told me, there are several programs you may be eligible for.",
    ]
    lines.append(random.choice(openers))
    lines.append("")

    def format_program(prog: dict, level: str) -> str:
        s = f"**{prog['program']}**\n"
        if level == "simple":
            s += f"This program could help you. {prog['reason']}.\n"
            if prog["benefit_amounts"]:
                amt = prog["benefit_amounts"]
                if len(amt) > 200:
                    amt = amt[:200].rsplit(".", 1)[0] + "."
                s += f"How much: {amt}\n"
        elif level == "standard":
            s += f"You may be eligible because: {prog['reason']}.\n"
            if prog["benefit_amounts"]:
                amt = prog["benefit_amounts"]
                if len(amt) > 300:
                    amt = amt[:300].rsplit(".", 1)[0] + "."
                s += f"Estimated benefits: {amt}\n"
        else:  # detailed
            s += f"Eligibility assessment: {prog['reason']}. Confidence: {prog['confidence']}.\n"
            if prog["benefit_amounts"]:
                s += f"Benefit details: {prog['benefit_amounts']}\n"
        return s

    if high_priority:
        lines.append("## Programs You Should Apply For First\n")
        for prog in high_priority:
            lines.append(format_program(prog, reading_level))

    if normal_priority:
        lines.append("## Also Worth Checking\n")
        for prog in normal_priority:
            lines.append(format_program(prog, reading_level))

    # Documents
    all_docs = set()
    for prog in eligible_programs:
        if prog["documents_required"]:
            for doc in prog["documents_required"].split(","):
                doc = doc.strip().strip(".")
                if doc:
                    all_docs.add(doc)
    if all_docs:
        lines.append("## Documents to Gather\n")
        for doc in sorted(all_docs)[:10]:
            lines.append(f"- {doc}")
        lines.append("")

    # Where to apply
    urls = {}
    for prog in eligible_programs:
        if prog["application_url"]:
            urls[prog["program"]] = prog["application_url"]
    if urls:
        lines.append("## Where to Apply\n")
        for name, url in urls.items():
            lines.append(f"- **{name}**: {url}")
        lines.append("")
        lines.append(f"You can also apply for most programs at **MNbenefits.mn.gov** or by calling **211**.")

    lines.append(RESPONSE_DISCLAIMER)

    return "\n".join(lines)


def generate_response_example(persona: dict, programs: list[dict]) -> dict | None:
    """Generate a plain language response training example."""
    eligible = check_eligibility(persona, programs)
    if not eligible:
        # Still generate some "no programs found" examples
        if random.random() > 0.3:
            return None

    reading_level = random.choice(READING_LEVELS)
    lang_code = persona["language"]
    lang_name = persona["language_name"]

    system_prompt = (
        f"You are a plain-language government benefits navigator. Your job is to explain "
        f"benefits eligibility results in clear, simple language.\n\n"
        f"TARGET READING LEVEL: {reading_level}\n"
        f"LANGUAGE: Respond in {lang_name}.\n\n"
        f"Structure your response as:\n"
        f"1. A brief empathetic acknowledgment\n"
        f"2. HIGH PRIORITY programs\n"
        f"3. ALSO CHECK programs\n"
        f"4. DOCUMENTS TO GATHER\n"
        f"5. WHERE TO APPLY\n\n"
        f"For each program, include the program name, why they may be eligible, "
        f"and estimated benefit amount if available.\n\n"
        f"CRITICAL: Only include programs from the provided eligibility results. "
        f"Never say someone \"qualifies\" — say \"may be eligible.\"\n"
        f"End with the standard disclaimer."
    )

    # User message is the eligibility results + persona summary
    user_msg = f"Here are the eligibility results for this person:\n\n"
    user_msg += f"Profile: {persona['age']} years old, {persona['household_desc']}, "
    user_msg += f"in {persona['county']} County, {persona['employment_status'].replace('_', ' ')}, "
    user_msg += f"income ${persona['income_monthly']:,}/month.\n\n"

    if eligible:
        user_msg += "Eligible programs:\n"
        for prog in eligible:
            user_msg += f"- {prog['program']}: {prog['reason']} (confidence: {prog['confidence']})\n"
    else:
        user_msg += "No programs matched the eligibility criteria.\n"

    user_msg += f"\nPlease generate a {reading_level}-level response in {lang_name}."

    response = format_response(persona, eligible, reading_level)

    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": response},
        ]
    }


# ---------------------------------------------------------------------------
# Category 3: Benefits Q&A
# ---------------------------------------------------------------------------

QA_SYSTEM = (
    "You are a plain-language government benefits navigator for Minnesota. "
    "You help people understand which government assistance programs they may "
    "be eligible for based on their situation. Be warm, clear, and actionable. "
    "Always cite specific eligibility thresholds and application portals. "
    'Never say someone "qualifies" — say "may be eligible." '
    "End every response with a disclaimer that this is informational, not legal advice."
)

QA_TEMPLATES = [
    # Program-specific questions
    ("What is {program_name}?",
     "overview"),
    ("How do I apply for {program_name}?",
     "application"),
    ("What documents do I need for {program_name}?",
     "documents"),
    ("What's the income limit for {program_name}?",
     "income_limit"),
    ("How much does {program_name} pay?",
     "benefit_amounts"),
    ("Am I eligible for {program_name} if I make ${income}/month with a family of {hh_size}?",
     "eligibility_check"),
    ("Can I get {program_name} if I'm not a citizen?",
     "citizenship"),
    ("I got denied for {program_name}. What can I do?",
     "denial"),
    ("How long does it take to get approved for {program_name}?",
     "timeline"),
    ("Can I get {program_name} and {program_name_2} at the same time?",
     "combo"),
    # General questions
    ("What help is available for someone who just lost their job?",
     "general_unemployment"),
    ("I need help with food. What programs are there?",
     "general_food"),
    ("What healthcare options do I have if I can't afford insurance?",
     "general_health"),
    ("I'm about to be evicted. What emergency help is there?",
     "general_emergency"),
    ("Where do I go to apply for benefits in {county} County?",
     "general_county"),
    ("What's the difference between Medical Assistance and MinnesotaCare?",
     "general_compare"),
    ("Do I need to report income changes while on {program_name}?",
     "reporting"),
    ("Can I get help with my heating bill?",
     "general_energy"),
]


def generate_qa_response(question_type: str, program: dict | None, persona: dict | None) -> str:
    """Generate a Q&A response based on question type and program data."""
    if program is None:
        # General question responses
        responses = {
            "general_unemployment": (
                "If you've recently lost your job, there are several programs that may help:\n\n"
                "**Unemployment Insurance (UI)**: If you were laid off through no fault of your own, "
                "you may be eligible for weekly UI benefits. Apply at uimn.org or call 651-296-3644.\n\n"
                "**SNAP/Food Assistance**: With reduced or no income, you may be eligible for food "
                "assistance. The income limit is 200% FPL under Minnesota's BBCE rules.\n\n"
                "**Medical Assistance**: If your income drops below 138% FPL, you may be eligible "
                "for free healthcare coverage.\n\n"
                "**MFIP**: If you have dependent children, the Minnesota Family Investment Program "
                "provides cash and food assistance.\n\n"
                "**Where to start**: Apply online at MNbenefits.mn.gov or call 211 for help."
            ),
            "general_food": (
                "Minnesota has several food assistance programs:\n\n"
                "**SNAP (Food Assistance)**: Monthly EBT benefits for groceries. Income limit is "
                "200% FPL (e.g., $2,608/mo for 1 person, $5,298/mo for family of 4). Apply at "
                "MNbenefits.mn.gov.\n\n"
                "**WIC**: For pregnant women, new mothers, and children under 5. Provides specific "
                "food items. Income limit 185% FPL.\n\n"
                "**Emergency Food Shelves**: No income requirements. Find locations at "
                "hungersolutions.org or call 211.\n\n"
                "**Free School Meals**: If your children qualify for SNAP or MFIP, they automatically "
                "get free school meals."
            ),
            "general_health": (
                "If you can't afford insurance, Minnesota has strong healthcare options:\n\n"
                "**Medical Assistance (MA)**: Free coverage if income is below 138% FPL "
                "(~$1,798/mo for 1 person). Covers most medical, dental, and mental health services.\n\n"
                "**MinnesotaCare**: Low-cost insurance for those between 138-200% FPL. Small monthly "
                "premiums based on income.\n\n"
                "**MNsure**: Minnesota's health insurance marketplace. You may qualify for subsidies "
                "to lower your premium.\n\n"
                "Apply for MA or MinnesotaCare at MNbenefits.mn.gov or MNsure.org."
            ),
            "general_emergency": (
                "If you're facing eviction or a housing emergency, act quickly:\n\n"
                "**Emergency Assistance (EA)**: Can help with rent, mortgage, or utility payments "
                "to prevent homelessness. Apply through your county human services office.\n\n"
                "**Emergency General Assistance (EGA)**: One-time cash payment for emergencies. "
                "Available to singles and couples without children.\n\n"
                "**211 Helpline**: Call or text 211 for immediate referrals to shelters and "
                "emergency services in your area.\n\n"
                "**Legal Aid**: If you've received an eviction notice, contact Legal Aid at "
                "mylegalaid.org for free legal help."
            ),
            "general_county": (
                f"In {persona['county'] if persona else 'your'} County, you can apply for most "
                "benefits in several ways:\n\n"
                "**Online**: MNbenefits.mn.gov — one application covers SNAP, cash assistance, "
                "healthcare, and childcare.\n\n"
                "**Phone**: Call 211 for help finding your county office.\n\n"
                "**In person**: Visit your county human services office. Bring ID, proof of income, "
                "and housing costs.\n\n"
                "Many counties also have community navigators who can help you apply."
            ),
            "general_compare": (
                "**Medical Assistance (MA)** and **MinnesotaCare** are both Minnesota health "
                "insurance programs, but they serve different income levels:\n\n"
                "**Medical Assistance**: For people with income below 138% FPL (~$1,798/mo for "
                "1 person). Completely free — no premiums, no copays for most services.\n\n"
                "**MinnesotaCare**: For people with income between 138-200% FPL (~$1,798-$2,608/mo "
                "for 1 person). Has small monthly premiums based on income, typically $0-$80/mo.\n\n"
                "Both cover doctor visits, prescriptions, mental health, and dental. If your "
                "income is low enough for MA, you'll automatically be enrolled in that instead "
                "of MinnesotaCare.\n\n"
                "Apply for either at MNbenefits.mn.gov — the system will determine which one "
                "you're eligible for."
            ),
            "general_energy": (
                "Yes! Minnesota has programs to help with heating and utility bills:\n\n"
                "**Energy Assistance Program (EAP)**: Helps pay heating costs. Income limit is "
                "200% FPL. Apply through your local CAP agency, usually October-May.\n\n"
                "**Weatherization**: Free home improvements (insulation, sealing) to reduce "
                "energy costs. Available through your local CAP agency.\n\n"
                "**Utility company programs**: Most MN utilities have low-income discount "
                "programs. Call your utility company to ask about rate reductions.\n\n"
                "**Cold Weather Rule**: From October 1 to April 30, utilities cannot disconnect "
                "your heat if you set up a payment plan. Call your utility to arrange this."
            ),
        }
        response = responses.get(question_type, "I'd be happy to help with that question. Could you tell me more about your specific situation so I can give you the most relevant information?")
        return response + RESPONSE_DISCLAIMER

    # Program-specific responses
    p = program
    if question_type == "overview":
        return (
            f"**{p['name']}**\n\n{p['description'][:500]}"
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "application":
        return (
            f"To apply for **{p['name']}**:\n\n"
            f"**Online**: {p.get('application_url', 'MNbenefits.mn.gov')}\n"
            f"**Phone**: Call 211 or your county human services office\n"
            f"**In person**: Visit your county human services office with required documents\n\n"
            f"The online application at MNbenefits.mn.gov is usually the fastest option."
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "documents":
        return (
            f"For **{p['name']}**, you'll generally need:\n\n"
            f"{p.get('documents_required', 'Contact your county office for a complete list.')}\n\n"
            f"Bring originals and copies when applying in person."
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "income_limit":
        return (
            f"**{p['name']}** income limits:\n\n"
            f"{p.get('eligibility_summary', 'Contact your county office for current limits.')}\n\n"
            f"Income limits are updated annually based on the Federal Poverty Level."
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "benefit_amounts":
        return (
            f"**{p['name']}** benefit amounts:\n\n"
            f"{p.get('benefit_amounts', 'Amounts vary based on household size and income.')}"
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "eligibility_check":
        income = persona["income_monthly"] if persona else 2000
        hh = persona["household_size"] if persona else 3
        eligible = check_eligibility(
            {"income_monthly": income, "household_size": hh,
             "employment_status": "employed", "dependents": persona.get("dependents", []) if persona else [],
             "concerns": [], "age": 30, "is_veteran": False, "is_disabled": False,
             "citizenship_status": "citizen", "county": "Hennepin", "language": "en"},
            [program]
        )
        if eligible:
            return (
                f"Based on an income of ${income:,}/month and household size of {hh}, "
                f"you may be eligible for **{p['name']}**.\n\n"
                f"{eligible[0]['reason']}.\n\n"
                f"To confirm, apply at {p.get('application_url', 'MNbenefits.mn.gov')}."
                + RESPONSE_DISCLAIMER
            )
        else:
            return (
                f"Based on an income of ${income:,}/month and household size of {hh}, "
                f"you may not meet the income requirements for **{p['name']}** at this time.\n\n"
                f"{p.get('eligibility_summary', '')[:200]}\n\n"
                f"However, I'd still recommend applying — there may be factors I'm not aware of. "
                f"Apply at {p.get('application_url', 'MNbenefits.mn.gov')}."
                + RESPONSE_DISCLAIMER
            )
    elif question_type == "citizenship":
        return (
            f"Eligibility for **{p['name']}** depends on immigration status:\n\n"
            f"- **U.S. citizens**: Eligible if meeting other requirements\n"
            f"- **Permanent residents (green card)**: Generally eligible, but some programs "
            f"have a 5-year waiting period\n"
            f"- **Refugees/asylees**: Usually eligible immediately\n"
            f"- **Undocumented**: Generally not eligible for most federal programs, but "
            f"children may be eligible for Emergency Medical Assistance\n\n"
            f"Minnesota has some state-funded programs that serve additional populations. "
            f"Contact your county office to discuss your specific situation — they can help "
            f"determine eligibility confidentially."
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "denial":
        return (
            f"If you were denied **{p['name']}**, you have options:\n\n"
            f"1. **Request a fair hearing**: You have 30 days to appeal. The denial notice "
            f"should include instructions.\n"
            f"2. **Contact Legal Aid**: Free legal help for benefits issues at mylegalaid.org\n"
            f"3. **Ask your county worker**: Sometimes denials are due to missing documents "
            f"that you can still provide.\n"
            f"4. **Reapply**: If your situation has changed, you can submit a new application.\n\n"
            f"Don't give up — many initial denials are overturned on appeal."
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "timeline":
        return (
            f"Processing times for **{p['name']}**:\n\n"
            f"- **SNAP**: Must be processed within 30 days. Expedited (7 days) if you have "
            f"very low income/resources.\n"
            f"- **Medical Assistance**: Usually processed within 45 days.\n"
            f"- **Other programs**: Typically 30-45 days.\n\n"
            f"You can check your application status through your county office or online."
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "reporting":
        return (
            f"Yes, you generally need to report changes while receiving **{p['name']}**:\n\n"
            f"- **Income changes**: Report within 10 days\n"
            f"- **Household size changes**: Report within 10 days\n"
            f"- **Address changes**: Report promptly\n"
            f"- **Employment changes**: Report within 10 days\n\n"
            f"Failing to report changes can result in overpayment that you'd have to pay back, "
            f"or loss of benefits. Report changes to your county worker."
            + RESPONSE_DISCLAIMER
        )
    elif question_type == "combo":
        return (
            f"Yes, in many cases you can receive multiple benefits at the same time! "
            f"Common combinations include:\n\n"
            f"- **SNAP + Medical Assistance**: Very common together\n"
            f"- **MFIP + CCAP**: Families on MFIP often get child care assistance too\n"
            f"- **SNAP + Energy Assistance**: Both based on similar income limits\n"
            f"- **MFIP + SNAP**: MFIP includes a food portion that coordinates with SNAP\n\n"
            f"Each program has its own eligibility rules, so qualifying for one doesn't "
            f"guarantee qualifying for another. Apply through MNbenefits.mn.gov — the system "
            f"will screen you for all programs at once."
            + RESPONSE_DISCLAIMER
        )

    return f"I'd be happy to help with your question about {p['name']}." + RESPONSE_DISCLAIMER


def generate_qa_example(programs: list[dict], persona: dict | None = None) -> dict:
    """Generate a benefits Q&A training example."""
    template, q_type = random.choice(QA_TEMPLATES)

    program = random.choice(programs)
    program2 = random.choice([p for p in programs if p["id"] != program["id"]])

    if persona is None:
        persona = generate_persona()

    # Format question
    question = template.format(
        program_name=program["name"],
        program_name_2=program2["name"],
        income=persona["income_monthly"],
        hh_size=persona["household_size"],
        county=persona["county"],
    )

    # Determine if this is a general or program-specific question
    if q_type.startswith("general_"):
        response = generate_qa_response(q_type, None, persona)
    else:
        response = generate_qa_response(q_type, program, persona)

    return {
        "messages": [
            {"role": "system", "content": QA_SYSTEM},
            {"role": "user", "content": question},
            {"role": "assistant", "content": response},
        ]
    }


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate Navigator training data")
    parser.add_argument("--output", type=str, default=str(OUTPUT_DEFAULT),
                        help="Output JSONL file path")
    parser.add_argument("--extraction", type=int, default=500,
                        help="Number of extraction examples")
    parser.add_argument("--response", type=int, default=1500,
                        help="Number of response generation examples")
    parser.add_argument("--qa", type=int, default=500,
                        help="Number of Q&A examples")
    parser.add_argument("--include-existing", action="store_true",
                        help="Prepend existing final.jsonl examples")
    args = parser.parse_args()

    programs = load_programs()
    print(f"Loaded {len(programs)} programs")

    all_examples = []

    # Optionally include existing hand-crafted examples
    if args.include_existing:
        existing_path = DATA_DIR / "training" / "final.jsonl"
        if existing_path.exists():
            with open(existing_path) as f:
                for line in f:
                    if line.strip():
                        all_examples.append(json.loads(line))
            print(f"Included {len(all_examples)} existing examples")

    # Category 1: Situation Extraction
    print(f"Generating {args.extraction} extraction examples...")
    for _ in range(args.extraction):
        persona = generate_persona()
        example = generate_extraction_example(persona)
        all_examples.append(example)

    # Category 2: Plain Language Response Generation
    print(f"Generating {args.response} response examples...")
    attempts = 0
    generated = 0
    while generated < args.response and attempts < args.response * 3:
        attempts += 1
        persona = generate_persona()
        example = generate_response_example(persona, programs)
        if example is not None:
            all_examples.append(example)
            generated += 1
    print(f"  Generated {generated} response examples ({attempts} attempts)")

    # Category 3: Benefits Q&A
    print(f"Generating {args.qa} Q&A examples...")
    for _ in range(args.qa):
        persona = generate_persona()
        example = generate_qa_example(programs, persona)
        all_examples.append(example)

    # Shuffle
    random.shuffle(all_examples)

    # Write
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        for example in all_examples:
            f.write(json.dumps(example) + "\n")

    print(f"\nTotal: {len(all_examples)} examples written to {output_path}")
    print(f"  Existing: {len(all_examples) - args.extraction - generated - args.qa if args.include_existing else 0}")
    print(f"  Extraction: {args.extraction}")
    print(f"  Response: {generated}")
    print(f"  Q&A: {args.qa}")

    # Stats
    total_tokens_est = 0
    for ex in all_examples:
        for msg in ex["messages"]:
            total_tokens_est += len(msg["content"].split()) * 1.3
    print(f"  Estimated tokens: ~{int(total_tokens_est):,}")


if __name__ == "__main__":
    main()
