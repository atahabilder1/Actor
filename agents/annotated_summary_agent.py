# agents/annotated_summary_agent.py

import openai
import os
from dotenv import load_dotenv
from core.base_agent import BaseAgent

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class AnnotatedSummaryAgent(BaseAgent):
    def run(self, contract_code):
        try:
            prompt = f"""You are a Solidity security expert. Analyze the following smart contract:
1. Annotate it line-by-line with inline comments (Solidity style).
2. Summarize its behavior and any security risks in plain language.

Contract:
{contract_code}
"""

            response = openai.ChatCompletion.create(
                model="gpt-4o",  # or "gpt-4-1106-preview"
                messages=[
                    {"role": "system", "content": "You are a smart contract auditor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            content = response["choices"][0]["message"]["content"]

            # Separate annotated code and summary if labeled
            if "Summary:" in content:
                annotated, summary = content.split("Summary:")
                annotated = annotated.strip()
                summary_points = [line.strip("-• \n") for line in summary.strip().splitlines() if line.strip()]
            else:
                annotated = content.strip()
                summary_points = []

            return [{
                "type": "LLMAnnotated",
                "message": "LLM-generated annotated code and summary.",
                "annotated_code": annotated,
                "points": summary_points
            }]

        except Exception as e:
            return [{
                "type": "Error",
                "message": f"LLM processing failed: {e}"
            }]
