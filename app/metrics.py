def compute_metrics(verification_results):
    total = len(verification_results)
    supported = sum(1 for r in verification_results if r["status"] == "SUPPORTED")
    contradicted = sum(1 for r in verification_results if r["status"] == "CONTRADICTED")

    return {
        "total_claims": total,
        "supported_rate": supported / total if total else 0,
        "contradicted_rate": contradicted / total if total else 0
    }
