from explainability.prompts import route_decision_prompt


class LLMReasoner:
    """
    Simulated LLM Reasoning Layer (Phase 6B)
    This will later be replaced with real LLM API calls.
    """

    def generate_reasoning(self, best_route, all_routes):
        rejected = [
            r for r in all_routes if r["route_id"] != best_route["route_id"]
        ]

        rejected_summary = ""
        for r in rejected:
            rejected_summary += (
                f"- Route {r['route_id']} | "
                f"ETA: {r['eta_min']} min | "
                f"Loss: ₹{r['total_loss']}\n"
            )

        prompt = route_decision_prompt(best_route, rejected_summary)

        # 🔒 Deterministic "LLM-style" reasoning (safe, auditable)
        reasoning = (
            f"The system selected route {best_route['route_id']} because it "
            f"results in the lowest overall operational loss. Compared to "
            f"alternative routes, it demonstrates a better balance between "
            f"delivery time, fuel expenditure, environmental impact, and risk.\n\n"
            f"Other routes were rejected due to higher delays, fuel costs, "
            f"carbon emissions, or SLA penalties, which significantly increased "
            f"their total expected loss. The decision prioritizes cost efficiency, "
            f"service reliability, and sustainability while minimizing operational risk."
        )

        return {
            "prompt_used": prompt,
            "llm_reasoning": reasoning
        }
