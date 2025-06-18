# agents/slither_agent.py

import subprocess
import json
import tempfile
import os
from core.base_agent import BaseAgent

class SlitherAgent(BaseAgent):
    def run(self, contract_code):
        results = []

        # Create a temporary Solidity file
        with tempfile.NamedTemporaryFile(suffix=".sol", delete=False, mode="w") as tmp_file:
            tmp_file.write(contract_code)
            temp_file_path = tmp_file.name

        # Temporary output file for Slither JSON results
        output_file = "slither-output.json"

        try:
            result = subprocess.run(
                ["slither", temp_file_path, "--json", output_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Allow Slither exit codes 0 (clean) and 1 (vulnerabilities)
            if result.returncode not in [0, 1]:
                return [{
                    "type": "Error",
                    "message": f"Slither execution failed:\n{result.stderr.strip()}"
                }]
        except Exception as e:
            return [{
                "type": "Error",
                "message": f"Exception while running Slither: {str(e)}"
            }]

        # Parse Slither output
        try:
            with open(output_file, "r") as f:
                data = json.load(f)

            for detector in data.get("results", {}).get("detectors", []):
                results.append({
                    "type": "Slither",
                    "message": detector.get("description", "No description provided.")
                })

        except Exception as e:
            results.append({
                "type": "Error",
                "message": f"Could not parse Slither output: {str(e)}"
            })

        # Clean up temp files
        try:
            os.remove(temp_file_path)
            os.remove(output_file)
        except Exception:
            pass  # Ignore cleanup errors

        return results
