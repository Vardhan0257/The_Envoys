import json
import time
import requests
import pandas as pd

NAIVE_URL = "http://localhost:8000/rag-naive"
VERIFIED_URL = "http://localhost:8000/rag-verified"

EVAL_FILE = "data/eval_questions.json"
OUTPUT_CSV = "logs/eval_results.csv"


def run_naive(question):
    start = time.time()
    resp = requests.post(NAIVE_URL, params={"question": question})
    latency = time.time() - start
    return resp.json(), latency


def run_verified(question):
    start = time.time()
    resp = requests.post(VERIFIED_URL, params={"question": question})
    latency = time.time() - start
    return resp.json(), latency


def evaluate():
    with open(EVAL_FILE, "r") as f:
        questions = json.load(f)

    rows = []

    for q in questions:
        question = q["question"]
        qtype = q.get("type", "unknown")

        # --- Naive ---
        naive_resp, naive_latency = run_naive(question)

        # Naive has no claim structure → treat as 1 unverified answer
        rows.append({
            "question": question,
            "type": qtype,
            "system": "naive",
            "unsupported_claim": 1,   # by definition unverifiable
            "latency": naive_latency
        })

        # --- Verified ---
        verified_resp, verified_latency = run_verified(question)

        results = verified_resp.get("results", [])

        for r in results:
            rows.append({
                "question": question,
                "type": qtype,
                "system": "verified",
                "unsupported_claim": 1 if r["status"] != "SUPPORTED" else 0,
                "latency": verified_latency
            })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False)

    print("Evaluation complete.")
    print(df.groupby("system")["unsupported_claim"].mean())
    print(f"Saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    evaluate()
