# agents/reentrancy_agent.py

from core.base_agent import BaseAgent

class ReentrancyAgent(BaseAgent):
    def run(self, contract_code):
        if "call{" in contract_code and "balances[msg.sender] = 0" in contract_code:
            return [{
                "type": "Reentrancy",
                "message": "Potential reentrancy vulnerability: call with value before balance update."
            }]
        return []
