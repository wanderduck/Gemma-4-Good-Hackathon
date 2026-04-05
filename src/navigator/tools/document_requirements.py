"""Document requirements lookup for benefits programs."""

from navigator.models import UserProfile

# Common documents by program. Sourced from MNbenefits.mn.gov FAQ and
# DHS Combined Manual application requirements.

_PROGRAM_DOCS = {
    "snap": [
        "Government-issued photo ID",
        "Proof of income (last 30 days pay stubs or employer letter)",
        "Proof of residency (utility bill, lease, or mail)",
        "Social Security numbers for all household members",
        "Bank statements (last 30 days)",
    ],
    "mfip": [
        "Government-issued photo ID",
        "Birth certificates for all children in household",
        "Proof of income (last 30 days pay stubs or employer letter)",
        "Social Security numbers for all household members",
        "Proof of residency (utility bill, lease, or mail)",
        "Bank statements (last 30 days)",
        "Proof of child care costs (if applicable)",
    ],
    "medical_assistance": [
        "Government-issued photo ID",
        "Social Security numbers for all household members",
        "Proof of income (last 30 days pay stubs or tax return)",
        "Proof of residency",
        "Immigration documents (if applicable)",
    ],
    "minnesotacare": [
        "Government-issued photo ID",
        "Social Security numbers for all household members",
        "Proof of income (last 30 days pay stubs or tax return)",
        "Proof of residency",
        "Proof that no affordable employer coverage is available",
    ],
    "unemployment_insurance": [
        "Government-issued photo ID",
        "Social Security number",
        "Employer name, address, and phone for last 18 months",
        "Layoff letter or separation notice (if available)",
        "Direct deposit bank information",
    ],
    "emergency_assistance": [
        "Government-issued photo ID",
        "Proof of emergency (eviction notice, utility shutoff notice)",
        "Proof of income",
        "Proof of residency",
        "Birth certificates for children",
    ],
    "ccap": [
        "Government-issued photo ID",
        "Proof of income (last 30 days)",
        "Proof of activity (work schedule, school enrollment, job search log)",
        "Child care provider information",
        "Birth certificates for children",
    ],
    "energy_assistance": [
        "Government-issued photo ID",
        "Social Security numbers for all household members",
        "Proof of income (last 30 days)",
        "Most recent utility bill",
        "Proof of residency",
    ],
    "dislocated_worker": [
        "Government-issued photo ID",
        "Proof of layoff (separation notice, WARN notice, or employer letter)",
        "Resume (if available)",
    ],
}


class DocumentRequirementsTool:
    """Look up required documents for benefits program applications."""

    def get_documents(self, program_id: str, profile: UserProfile) -> list[str]:
        """Get required documents for a specific program."""
        docs = list(_PROGRAM_DOCS.get(program_id, []))

        # Add conditional documents based on profile
        if profile.citizenship_status != "citizen":
            docs.append("Immigration/citizenship documentation")
        if profile.is_disabled:
            docs.append("Disability documentation or SSI/SSDI award letter")
        if profile.is_veteran:
            docs.append("DD-214 or VA documentation")

        return docs

    def get_consolidated_documents(
        self, program_ids: list[str], profile: UserProfile
    ) -> list[str]:
        """Get a deduplicated, consolidated document list across multiple programs."""
        all_docs = []
        for pid in program_ids:
            all_docs.extend(self.get_documents(pid, profile))

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for doc in all_docs:
            if doc not in seen:
                seen.add(doc)
                unique.append(doc)
        return unique
