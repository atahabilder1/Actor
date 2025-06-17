# agents/integer_overflow_agent.py

from core.base_agent import BaseAgent

class IntegerOverflowAgent(BaseAgent):
    def run(self, contract_code):
        issues = []
        if any(op in contract_code for op in ["+", "-", "*", "/"]):
            if "SafeMath" not in contract_code and "unchecked" not in contract_code:
                issues.append({
                    "type": "IntegerOverflow",
                    "message": "Math operations detected without SafeMath or unchecked block."
                })
        return issues
