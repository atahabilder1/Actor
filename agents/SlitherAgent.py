# agents/slither_agent.py

import subprocess
import json
from core.base_agent import BaseAgent

class SlitherAgent(BaseAgent):
    def run(self, contract_code):
        # Save contract temporarily
        with open("temp_contract.sol", "w") as f:
            f.write(contract_code)

        # Run Slither
        try:
            subprocess.run(
                ["slither", "temp_contract.sol", "--json", "slither-output.json"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            return [{"type": "Error", "message": "Slither analysis failed."}]

        # Parse results
        try:
            with open("slither-output.json", "r") as f:
                data = json.load(f)
        except Exception as e:
            return [{"type": "Error", "message": f"Failed to parse Slither output: {e}"}]

        issues = []
        for detector in data.get("results", {}).get("detectors", []):
            issues.append({
                "type": "Slither",
                "message": f"{detector['check']} in {detector['elements'][0].get('name', '')}: {detector['description']}"
            })

        return issues
