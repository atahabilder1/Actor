# agents/slither_agent.py

import subprocess
import json
from core.base_agent import BaseAgent

class SlitherAgent(BaseAgent):
    def run(self, contract_code):
        temp_file = "temp_contract.sol"
        output_file = "slither-output.json"

        # Write contract code to a temp file
        with open(temp_file, "w") as f:
            f.write(contract_code)

        try:
            subprocess.run(
                ["slither", temp_file, "--json", output_file],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            return [{"type": "Error", "message": "Slither execution failed"}]

        # Parse Slither output
        try:
            with open(output_file, "r") as f:
                data = json.load(f)
        except Exception as e:
            return [{"type": "Error", "message": f"Could not parse Slither output: {e}"}]

        results = []
        for detector in data.get("results", {}).get("detectors", []):
            results.append({
                "type": "Slither",
                "message": detector.get("description", "No description provided.")
            })

        return results
