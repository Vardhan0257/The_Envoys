from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/deberta-v3-base-mnli"
)
model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-base-mnli"
)
model.eval()

LABELS = ["CONTRADICTION", "NEUTRAL", "ENTAILMENT"]

def verify_claim(claim: str, evidence: str):
    inputs = tokenizer(
        evidence,
        claim,
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=1)[0]

    result = {
        "entailment": probs[2].item(),
        "contradiction": probs[0].item(),
        "neutral": probs[1].item(),
    }

    if result["entailment"] > 0.7:
        status = "SUPPORTED"
    elif result["contradiction"] > 0.5:
        status = "CONTRADICTED"
    else:
        status = "INSUFFICIENT"

    return status, result
