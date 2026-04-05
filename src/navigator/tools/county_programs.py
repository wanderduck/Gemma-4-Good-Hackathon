"""County-specific program lookup for the five Twin Cities metro counties."""

# Hardcoded county data from research. In production, this would come from
# the scraped county pages in the knowledge base.

_COUNTY_DATA = {
    "ramsey": {
        "programs": [
            {
                "name": "Ramsey County Dislocated Worker Program",
                "type": "employment",
                "url": "https://www.ramseycountymn.gov/residents/assistance-support/employment-assistance/job-seeker-programs/dislocated-worker-program",
                "application_url": "https://www.ramseycountymn.gov/residents/assistance-support/employment-assistance/job-seeker-programs/dislocated-worker-program/dislocated-worker-program-application",
                "description": "County-run program for recently laid-off workers. Career exploration, skills assessment, resume writing, interview prep, training. Has its own application (5 business day response).",
                "phone": "651-266-3800",
            },
            {
                "name": "Ramsey County Emergency Assistance",
                "type": "emergency",
                "url": "https://www.ramseycountymn.gov/residents/assistance-support/assistance/financial-assistance/emergency-assistance",
                "description": "Short-term emergency assistance for rent, housing, and utilities.",
            },
        ],
        "cap": {
            "name": "CAPRW (Community Action Partnership of Ramsey & Washington Counties)",
            "url": "https://www.caprw.org/",
            "phone": "(651) 645-6445",
            "address": "450 Syndicate St N, Saint Paul, MN 55104",
            "programs": [
                "Energy Assistance (EAP)",
                "Head Start & Early Head Start",
                "SNAP Screening & Application Assistance",
                "Car Loan Program",
                "VITA Free Tax Clinic",
                "Section 8 Housing Applications (when waitlist opens)",
                "Financial Literacy Classes",
            ],
        },
        "phone_24_7": "651-266-3800 (24/7 EZ Info — English, Spanish, Hmong, Somali, Karen)",
        "application_portal": "MNbenefits.mn.gov",
    },
    "hennepin": {
        "programs": [
            {
                "name": "Hennepin Pathways Employment Program",
                "type": "employment",
                "url": "https://www.hennepin.us/pathways-program",
                "description": "County employment program placing graduates in county jobs (office admin, human services, building ops).",
            },
            {
                "name": "Hennepin County SNAP Employment & Training",
                "type": "employment",
                "url": "https://www.hennepin.us/residents/human-services/workforce-development",
                "description": "Job resources, support, and training for SNAP recipients.",
            },
        ],
        "cap": {
            "name": "CAP-HC (Community Action Partnership of Hennepin County)",
            "url": "https://caphennepin.org/",
            "phone": "See website",
            "programs": [
                "Energy Assistance",
                "Water Assistance",
                "Rental Assistance",
                "Vehicle Repair Program",
                "Homebuyer Services",
                "Tax Assistance",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
    "dakota": {
        "programs": [
            {
                "name": "Dakota County Emergency Assistance",
                "type": "emergency",
                "url": "https://www.co.dakota.mn.us/HealthFamily/PublicAssistance/Emergency/Pages/default.aspx",
                "description": "One-time payment for eviction or utility shutoff.",
                "phone": "651-554-5611",
            },
        ],
        "cap": {
            "name": "CAP Agency (Scott-Carver-Dakota)",
            "url": "https://capagency.org/",
            "phone": "651-322-3500",
            "address": "2496 145th St W, Rosemount, MN 55068",
            "programs": [
                "Energy Assistance",
                "Emergency Furnace Repair/Replacement",
                "Head Start (ages 3-5)",
                "Early Head Start (birth-3)",
                "Chore Program for Seniors",
                "Housing Services",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
    "scott": {
        "programs": [],
        "cap": {
            "name": "CAP Agency (Scott-Carver-Dakota)",
            "url": "https://capagency.org/",
            "phone": "See Shakopee office",
            "address": "738 1st Ave E, Shakopee, MN 55379",
            "programs": [
                "Energy Assistance",
                "Emergency Furnace Repair/Replacement",
                "Head Start",
                "Early Head Start",
                "Housing Services",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
    "carver": {
        "programs": [],
        "cap": {
            "name": "CAP Agency (Scott-Carver-Dakota)",
            "url": "https://capagency.org/",
            "phone": "952-496-2125",
            "address": "110 W 2nd St, Chaska, MN 55318",
            "programs": [
                "Energy Assistance",
                "Emergency Furnace Repair/Replacement",
                "Head Start",
                "Housing Services",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
}


class CountyProgramsTool:
    """Look up county-specific programs and CAP agencies."""

    def get_programs(self, county: str) -> list[dict]:
        """Get all county-specific programs for a given county."""
        data = _COUNTY_DATA.get(county.lower())
        if not data:
            return []

        results = []
        for prog in data.get("programs", []):
            results.append(prog)

        # Add CAP agency programs
        cap = data.get("cap")
        if cap:
            results.append({
                "name": cap["name"],
                "type": "cap",
                "url": cap["url"],
                "phone": cap.get("phone", ""),
                "description": f"Programs: {', '.join(cap['programs'])}",
            })

        return results

    def get_cap_agency(self, county: str) -> dict | None:
        """Get the CAP agency serving a given county."""
        data = _COUNTY_DATA.get(county.lower())
        if not data:
            return None
        return data.get("cap")

    def get_application_portal(self, county: str) -> str:
        """Get the primary application portal for a county."""
        data = _COUNTY_DATA.get(county.lower())
        if not data:
            return "MNbenefits.mn.gov"
        return data.get("application_portal", "MNbenefits.mn.gov")
