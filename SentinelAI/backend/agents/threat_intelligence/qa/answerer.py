"""Threat intelligence question answering."""

from agents.threat_intelligence.langchain_adapter import build_threat_intel_prompt


class ThreatIntelAnswerer:
    """Generate grounded answers from retrieved context."""

    def answer(self, question: str, retrieved_chunks: list[dict]) -> dict:
        """Return an answer with citations and technique explanation."""
        context_lines = []
        citations = []
        techniques = []

        for result in retrieved_chunks:
            document = result["document"]
            citations.append(
                {
                    "source": document.source,
                    "title": document.title,
                    "citation": document.citation,
                    "score": round(result["score"], 4),
                }
            )
            context_lines.append(f"[{document.source}] {document.content}")
            if "T" in document.content and ("technique" in document.content.lower() or "mitre" in document.source):
                techniques.append(document.title)

        if not retrieved_chunks:
            return {
                "answer": "No relevant threat intelligence context was found in the current vector store.",
                "attack_techniques": [],
                "citations": [],
            }

        build_threat_intel_prompt(question=question, context="\n\n".join(context_lines))
        answer = (
            "Based on the retrieved threat intelligence, the likely security context is: "
            f"{' '.join(context_lines)[:1200]}"
        )
        if "explain" in question.lower() or "technique" in question.lower() or "attack" in question.lower():
            answer += " The referenced attack techniques should be mapped to observed tactics, affected assets, and available mitigations before response actions are taken."

        return {
            "answer": answer,
            "attack_techniques": sorted(set(techniques)),
            "citations": citations,
        }
