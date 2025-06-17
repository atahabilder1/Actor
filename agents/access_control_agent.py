# agents/access_control_agent.py

import re
from core.base_agent import BaseAgent

class AccessControlAgent(BaseAgent):
    def run(self, contract_code):
        issues = []
        lines = contract_code.splitlines()

        for i, line in enumerate(lines, start=1):
            # Look for public or external functions
            if re.search(r"\bfunction\b.*\b(public|external)\b", line):
                if not re.search(r"\bonlyOwner\b|\brequire\s*\(\s*msg\.sender\b", line):
                    func_name_match = re.search(r"function\s+([a-zA-Z0-9_]+)", line)
                    func_name = func_name_match.group(1) if func_name_match else "unknown"

                    issues.append({
                        "type": "AccessControl",
                        "line": i,
                        "message": f"`{func_name}` may lack access control modifiers or ownership checks.",
                        "suggestion": "Consider adding `onlyOwner`, `access modifiers`, or appropriate `require(msg.sender == ...)` statements."
                    })

        return issues
