"""Benefits knowledge base search tool for the eligibility engine."""

from navigator.rag.retrieval import HybridRetriever
from navigator.config import TOP_K_FINAL


class BenefitsSearchTool:
    """Searches the benefits knowledge base using hybrid retrieval."""

    def __init__(self, retriever: HybridRetriever):
        self.retriever = retriever

    def search(
        self,
        query: str,
        state: str = "MN",
        county: str | None = None,
        category: str | None = None,
        top_k: int = TOP_K_FINAL,
    ) -> list[dict]:
        """Search the benefits KB for relevant programs.

        Automatically includes federal programs and filters by state/county.
        """
        jurisdictions = ["federal", f"state:{state}"]
        if county:
            jurisdictions.append(f"county:{county.lower()}")
            cap_map = {
                "ramsey": "cap:caprw",
                "hennepin": "cap:cap-hc",
                "dakota": "cap:cap-agency",
                "scott": "cap:cap-agency",
                "carver": "cap:cap-agency",
            }
            if county.lower() in cap_map:
                jurisdictions.append(cap_map[county.lower()])

        results = self.retriever.search(
            query=query,
            top_k=top_k,
            jurisdiction_filter=jurisdictions,
        )

        return results
