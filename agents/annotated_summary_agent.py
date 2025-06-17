# agents/annotated_summary_agent.py

from core.base_agent import BaseAgent

class AnnotatedSummaryAgent(BaseAgent):
    def run(self, contract_code):
        lines = contract_code.strip().splitlines()
        annotated_lines = []
        summary = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            if "call{" in stripped:
                annotated_lines.append(f"{line} // 🔥 external call with value")
                summary.append("Detected use of low-level call with value (possible reentrancy risk).")
            elif "require(" in stripped:
                annotated_lines.append(f"{line} // ✅ input or state validation")
                summary.append("Require statement found for enforcing conditions.")
            elif "msg.sender" in stripped:
                annotated_lines.append(f"{line} // 🧑 identifies caller address")
                summary.append("Detected use of msg.sender, likely for access or transfer.")

            else:
                annotated_lines.append(line)

        return [{
            "type": "AnnotatedCode",
            "message": "Annotated Solidity code with inline comments.",
            "annotated_code": "\n".join(annotated_lines)
        }, {
            "type": "Summary",
            "message": "Natural language summary of contract behavior.",
            "points": summary
        }]
