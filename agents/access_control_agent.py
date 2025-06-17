# agents/access_control_agent.py

from core.base_agent import BaseAgent

class AccessControlAgent(BaseAgent):
    def run(self, contract_code):
        issues = []
        lines = contract_code.splitlines()
        for line in lines:
            if "function " in line and ("public" in line or "external" in line):
                if "onlyOwner" not in line and "require(msg.sender" not in line:
                    issues.append({
                        "type": "AccessControl",
                        "message": f"Function may lack access control: {line.strip()}"
                    })
        return issues
