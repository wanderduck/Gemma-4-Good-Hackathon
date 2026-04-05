"""Stage 2: Eligibility Engine — determine which programs a user may qualify for.

Uses a hybrid approach:
- Hard-coded rule checks for well-defined thresholds (FPL, age, employment status)
- RAG search for additional programs and detailed eligibility context
- Function calling for external API data (when available)
"""

import logging
from navigator.models import UserProfile, EligibilityResult, BenefitsResponse
from navigator.tools.fpl import check_fpl_threshold
from navigator.tools.county_programs import CountyProgramsTool
from navigator.tools.document_requirements import DocumentRequirementsTool
from navigator.tools.benefits_search import BenefitsSearchTool

logger = logging.getLogger(__name__)


class EligibilityEngine:
    """Determines program eligibility for a given user profile."""

    def __init__(
        self,
        search_tool: BenefitsSearchTool | None = None,
        county_tool: CountyProgramsTool | None = None,
        doc_tool: DocumentRequirementsTool | None = None,
    ):
        self.search_tool = search_tool
        self.county_tool = county_tool or CountyProgramsTool()
        self.doc_tool = doc_tool or DocumentRequirementsTool()

    def evaluate(self, profile: UserProfile) -> BenefitsResponse:
        """Run full eligibility evaluation for a user profile.

        Returns a BenefitsResponse with all eligible programs, documents, and
        application groupings.
        """
        # Step 1: Rule-based checks for major programs
        results = self._run_rule_checks(profile)

        # Step 2: Add county-specific programs
        if profile.county:
            county_results = self._check_county_programs(profile)
            results.extend(county_results)

        # Step 3: Sort by priority
        priority_order = {"high": 0, "normal": 1, "low": 2}
        results.sort(key=lambda r: priority_order.get(r.priority, 1))

        # Step 4: Get consolidated documents
        eligible_ids = [r.program_id for r in results if r.eligible]
        documents = self.doc_tool.get_consolidated_documents(eligible_ids, profile)

        # Step 5: Group by application portal
        app_groups = self._group_by_portal(results)

        return BenefitsResponse(
            eligible_programs=[r for r in results if r.eligible],
            documents_needed=documents,
            application_groups=app_groups,
        )

    def _run_rule_checks(self, profile: UserProfile) -> list[EligibilityResult]:
        """Run all hard-coded eligibility rule checks."""
        checks = [
            self._check_snap,
            self._check_mfip,
            self._check_medical_assistance,
            self._check_minnesotacare,
            self._check_unemployment,
            self._check_emergency_assistance,
            self._check_ega,
            self._check_ccap,
            self._check_energy_assistance,
            self._check_wic,
        ]
        results = []
        for check in checks:
            try:
                result = check(profile)
                results.append(result)
            except Exception as e:
                logger.warning("Rule check %s failed: %s", check.__name__, e)
        return results

    def _check_snap(self, profile: UserProfile) -> EligibilityResult:
        """SNAP: MN uses BBCE with 200% FPL gross income limit."""
        if profile.income is None:
            return EligibilityResult(
                program_id="snap", program_name="SNAP (Food Assistance)",
                eligible=None, confidence="low", category="food",
                reason="Income information needed to determine eligibility.",
                priority="high",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 200)
        eligible = fpl["below_threshold"]
        return EligibilityResult(
            program_id="snap", program_name="SNAP (Food Assistance)",
            eligible=eligible, confidence="high", category="food",
            reason=f"Household income ${profile.income:,.0f} = {fpl['fpl_percentage']}% FPL. "
                   f"MN SNAP uses 200% FPL BBCE threshold. "
                   f"{'Below' if eligible else 'Above'} threshold.",
            estimated_benefit=self._estimate_snap_benefit(profile.household_size) if eligible else "",
            source="DHS Combined Manual Section 0007.06",
            priority="high" if eligible else "low",
        )

    def _check_mfip(self, profile: UserProfile) -> EligibilityResult:
        """MFIP: MN's TANF. Families with children in poverty."""
        if not profile.has_children:
            return EligibilityResult(
                program_id="mfip", program_name="MFIP (Cash & Food Assistance)",
                eligible=False, confidence="high", category="cash",
                reason="MFIP requires minor children in the household.",
                priority="low",
            )
        if profile.income is None:
            return EligibilityResult(
                program_id="mfip", program_name="MFIP (Cash & Food Assistance)",
                eligible=None, confidence="low", category="cash",
                reason="Income information needed.", priority="high",
            )
        # MFIP gross income limit is ~115% FPL at application; use 130% to capture
        # families near the line (exit standard is higher, ~160% FPL)
        fpl = check_fpl_threshold(profile.income, profile.household_size, 130)
        return EligibilityResult(
            program_id="mfip", program_name="MFIP (Cash & Food Assistance)",
            eligible=fpl["below_threshold"],
            confidence="medium",  # MFIP has asset tests we can't check
            category="cash",
            reason=f"MFIP serves families with children below poverty level. "
                   f"Income {fpl['fpl_percentage']}% FPL. Asset limit $10,000 (not verified).",
            source="MN Statutes Chapter 256J",
            priority="high" if fpl["below_threshold"] else "low",
        )

    def _check_medical_assistance(self, profile: UserProfile) -> EligibilityResult:
        """Medical Assistance (Medicaid): 138% FPL for adults 19-64."""
        if profile.income is None:
            return EligibilityResult(
                program_id="medical_assistance", program_name="Medical Assistance (Medicaid)",
                eligible=None, confidence="low", category="health",
                reason="Income information needed.", priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 138)
        return EligibilityResult(
            program_id="medical_assistance", program_name="Medical Assistance (Medicaid)",
            eligible=fpl["below_threshold"],
            confidence="high", category="health",
            reason=f"MA threshold: 138% FPL. Income = {fpl['fpl_percentage']}% FPL. "
                   f"{'Below' if fpl['below_threshold'] else 'Above'} threshold.",
            estimated_benefit="Free health coverage (no premium, $1-$3 copays)" if fpl["below_threshold"] else "",
            source="MN Statutes Chapter 256B; DHS EPM",
            priority="high" if fpl["below_threshold"] else "normal",
        )

    def _check_minnesotacare(self, profile: UserProfile) -> EligibilityResult:
        """MinnesotaCare: 138-200% FPL, ages 19-64."""
        if profile.income is None:
            return EligibilityResult(
                program_id="minnesotacare", program_name="MinnesotaCare",
                eligible=None, confidence="low", category="health",
                reason="Income information needed.", priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 200)
        above_138 = not check_fpl_threshold(profile.income, profile.household_size, 138)["below_threshold"]
        eligible = fpl["below_threshold"] and above_138
        return EligibilityResult(
            program_id="minnesotacare", program_name="MinnesotaCare",
            eligible=eligible,
            confidence="medium", category="health",
            reason=f"MinnesotaCare: 138-200% FPL. Income = {fpl['fpl_percentage']}% FPL. "
                   f"{'Within' if eligible else 'Outside'} range. Requires no affordable employer coverage.",
            source="MN Statutes Chapter 256L",
            priority="normal",
        )

    def _check_unemployment(self, profile: UserProfile) -> EligibilityResult:
        """Unemployment Insurance: recently lost job through no fault."""
        recently_unemployed = profile.employment_status in (
            "recently_unemployed", "long_term_unemployed"
        )
        return EligibilityResult(
            program_id="unemployment_insurance",
            program_name="Unemployment Insurance",
            eligible=recently_unemployed,
            confidence="medium" if recently_unemployed else "high",
            category="employment",
            reason=(
                "UI available for workers who lost their job through no fault of their own. "
                f"Employment status: {profile.employment_status or 'unknown'}. "
                "Must have sufficient work history (not verified)."
                if recently_unemployed else
                f"Employment status '{profile.employment_status}' does not indicate recent job loss."
            ),
            source="MN Statutes Chapter 268",
            priority="high" if recently_unemployed else "low",
        )

    def _check_emergency_assistance(self, profile: UserProfile) -> EligibilityResult:
        """Emergency Assistance: families with children facing housing crisis."""
        has_kids = profile.has_children
        housing_concern = "housing" in profile.concerns or "emergency" in profile.concerns
        eligible = has_kids and housing_concern
        return EligibilityResult(
            program_id="emergency_assistance",
            program_name="Emergency Assistance (EA)",
            eligible=eligible if (has_kids and housing_concern) else None,
            confidence="medium" if eligible else "low",
            category="emergency",
            reason="EA provides one-time payment for rent/mortgage/utilities for families "
                   "with children facing housing crisis. "
                   + ("Housing concern indicated." if housing_concern else "No housing crisis indicated.")
                   + (" Has children." if has_kids else " No children (EA requires children)."),
            source="DCYF Emergency Assistance program",
            priority="high" if eligible else "low",
        )

    def _check_ega(self, profile: UserProfile) -> EligibilityResult:
        """Emergency General Assistance: single adults, 200% FPL, emergency."""
        if profile.income is None:
            return EligibilityResult(
                program_id="ega", program_name="Emergency General Assistance (EGA)",
                eligible=None, confidence="low", category="emergency",
                reason="Income information needed.", priority="low",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 200)
        has_emergency = any(c in profile.concerns for c in ["housing", "food", "emergency", "energy"])
        eligible = fpl["below_threshold"] and has_emergency and not profile.has_children
        return EligibilityResult(
            program_id="ega", program_name="Emergency General Assistance (EGA)",
            eligible=eligible,
            confidence="medium", category="emergency",
            reason="EGA: one-time emergency help for individuals without children. "
                   f"Income {fpl['fpl_percentage']}% FPL (limit 200%). "
                   f"{'Emergency indicated.' if has_emergency else 'No emergency indicated.'} "
                   f"{'No children (eligible).' if not profile.has_children else 'Has children (use EA instead).'}",
            source="MN Statutes Chapter 256D; LawHelp MN",
            priority="normal" if eligible else "low",
        )

    def _check_ccap(self, profile: UserProfile) -> EligibilityResult:
        """CCAP: child care assistance for working/training parents."""
        has_young_kids = profile.has_children
        working_or_training = profile.employment_status in (
            "employed", "recently_unemployed", "student"
        )
        eligible = has_young_kids and working_or_training
        return EligibilityResult(
            program_id="ccap", program_name="Child Care Assistance Program (CCAP)",
            eligible=eligible if has_young_kids else False,
            confidence="medium" if eligible else "high",
            category="childcare",
            reason="CCAP helps pay for child care while parents work, look for work, or attend school. "
                   f"{'Has children.' if has_young_kids else 'No children.'} "
                   f"Income must be below 47% SMI (entry) / 85% SMI (exit). Income threshold not verified.",
            source="DCYF CCAP; MN House Research",
            priority="normal" if eligible else "low",
        )

    def _check_energy_assistance(self, profile: UserProfile) -> EligibilityResult:
        """Energy Assistance Program: 50% SMI income threshold."""
        # 50% SMI is roughly 60% FPL for most household sizes (approximation)
        if profile.income is None:
            return EligibilityResult(
                program_id="energy_assistance", program_name="Energy Assistance Program (EAP)",
                eligible=None, confidence="low", category="energy",
                reason="Income information needed.", priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 150)
        return EligibilityResult(
            program_id="energy_assistance", program_name="Energy Assistance Program (EAP)",
            eligible=fpl["below_threshold"],
            confidence="medium",  # Using FPL approximation for SMI
            category="energy",
            reason=f"EAP threshold: 50% State Median Income (approx 150% FPL). "
                   f"Income = {fpl['fpl_percentage']}% FPL. Benefits: $200-$1,400 heating, up to $600 crisis. "
                   f"Application deadline May 31, 2026.",
            source="MN Commerce Dept EAP Guidelines",
            priority="normal" if fpl["below_threshold"] else "low",
        )

    def _check_wic(self, profile: UserProfile) -> EligibilityResult:
        """WIC: pregnant/postpartum/children under 5, 185% FPL."""
        has_young = profile.has_young_children
        if not has_young:
            return EligibilityResult(
                program_id="wic", program_name="WIC (Women, Infants, and Children)",
                eligible=False, confidence="high", category="food",
                reason="WIC requires pregnant/postpartum women or children under 5.",
                priority="low",
            )
        if profile.income is None:
            return EligibilityResult(
                program_id="wic", program_name="WIC (Women, Infants, and Children)",
                eligible=None, confidence="low", category="food",
                reason="Income needed. Auto-eligible if on SNAP, Medicaid, or MFIP.",
                priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 185)
        return EligibilityResult(
            program_id="wic", program_name="WIC (Women, Infants, and Children)",
            eligible=fpl["below_threshold"],
            confidence="high", category="food",
            reason=f"WIC threshold: 185% FPL. Income = {fpl['fpl_percentage']}% FPL. "
                   f"Has child(ren) under 5. Also auto-eligible if receiving SNAP, MA, or MFIP.",
            source="MN Dept of Health WIC Program",
            priority="normal" if fpl["below_threshold"] else "low",
        )

    def _check_county_programs(self, profile: UserProfile) -> list[EligibilityResult]:
        """Check for county-specific programs."""
        results = []
        county_programs = self.county_tool.get_programs(profile.county or "")

        for prog in county_programs:
            if prog["type"] == "employment" and profile.employment_status in (
                "recently_unemployed", "long_term_unemployed"
            ):
                results.append(EligibilityResult(
                    program_id=f"county_{prog['name'].lower().replace(' ', '_')[:30]}",
                    program_name=prog["name"],
                    eligible=True,
                    confidence="medium",
                    category="employment",
                    reason=prog.get("description", "County employment program for displaced workers."),
                    source=prog.get("url", ""),
                    priority="normal",
                ))
            elif prog["type"] == "cap":
                results.append(EligibilityResult(
                    program_id=f"cap_{profile.county.lower() if profile.county else 'unknown'}",
                    program_name=prog["name"],
                    eligible=True,
                    confidence="high",
                    category="community",
                    reason=prog.get("description", "Community Action programs available to all residents."),
                    source=prog.get("url", ""),
                    priority="normal",
                ))

        return results

    def _estimate_snap_benefit(self, household_size: int) -> str:
        """Rough SNAP benefit estimate by household size (2026 values)."""
        estimates = {1: "$292", 2: "$535", 3: "$768", 4: "$975", 5: "$1,158", 6: "$1,390"}
        return f"Up to {estimates.get(household_size, '$' + str(292 + 243 * (household_size - 1)))}/month"

    def _group_by_portal(self, results: list[EligibilityResult]) -> dict[str, list[str]]:
        """Group eligible programs by application portal."""
        portal_map = {
            "snap": "MNbenefits.mn.gov",
            "mfip": "MNbenefits.mn.gov",
            "emergency_assistance": "MNbenefits.mn.gov",
            "ega": "MNbenefits.mn.gov",
            "ccap": "MNbenefits.mn.gov",
            "medical_assistance": "MNsure.org",
            "minnesotacare": "MNsure.org",
            "unemployment_insurance": "uimn.org",
            "energy_assistance": "Contact local CAP agency",
            "wic": "Call 1-800-942-4030",
        }
        groups: dict[str, list[str]] = {}
        for r in results:
            if not r.eligible:
                continue
            portal = portal_map.get(r.program_id, "Contact county office")
            if portal not in groups:
                groups[portal] = []
            groups[portal].append(r.program_name)
        return groups
