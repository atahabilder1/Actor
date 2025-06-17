# agents/static_analyzer_agent.py

from core.base_agent import BaseAgent

class GeneralStaticAnalyzerAgent(BaseAgent):
    def run(self, contract_code):
        issues = []
        if "tx.origin" in contract_code:
            issues.append({
                "type": "Security",
                "message": "Usage of tx.origin is discouraged due to phishing risk."
            })
        if "delegatecall" in contract_code:
            issues.append({
                "type": "Security",
                "message": "Usage of delegatecall can be dangerous if unchecked."
            })
        return issues
