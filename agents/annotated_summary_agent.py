# agents/annotated_summary_agent.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from core.base_agent import BaseAgent

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class AnnotatedSummaryAgent(BaseAgent):
    def run(self, contract_code):
        try:
            prompt = f"""You are a Solidity security expert. Analyze the following smart contract:
1. Annotate it line-by-line with inline comments (Solidity style).
2. Summarize its behavior and any security risks in plain language.

Contract:
{contract_code}
"""

            response = client.chat.completions.create(
                model="gpt-4o",  # You can change to "gpt-4" or "gpt-3.5-turbo" if needed
                messages=[
                    {"role": "system", "content": "You are a smart contract auditor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            content = response.choices[0].message.content.strip()

            # Separate annotated code and summary if present
            if "Summary:" in content:
                annotated, summary = content.split("Summary:", 1)
                annotated = annotated.strip()
                summary_points = [line.strip("-• \n") for line in summary.strip().splitlines() if line.strip()]
            else:
                annotated = content
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
