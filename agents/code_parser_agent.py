# agents/code_parser_agent.py

from core.base_agent import BaseAgent

class CodeParserAgent(BaseAgent):
    def run(self, contract_code):
        # In a real parser, you'd analyze AST or structure.
        # For demo purposes, simulate function and call detection.
        functions = []
        for line in contract_code.splitlines():
            line = line.strip()
            if line.startswith("function "):
                functions.append(line)

        return [{
            "type": "Info",
            "message": f"Detected {len(functions)} function(s)",
            "details": functions
        }]
