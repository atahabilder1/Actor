# agentic_audit_system.py

import os
from agents.code_parser_agent import CodeParserAgent
from agents.reentrancy_agent import ReentrancyAgent
from agents.integer_overflow_agent import IntegerOverflowAgent
from agents.access_control_agent import AccessControlAgent
from agents.static_analyzer_agent import GeneralStaticAnalyzerAgent
from agents.test_case_generator_agent import TestCaseGeneratorAgent
from agents.annotated_summary_agent import AnnotatedSummaryAgent
from agents.slither_agent import SlitherAgent
from agents.compliance_coordinator_agent import ComplianceCoordinatorAgent

from core.audit_store import AuditStore
from core.message_queue import MessageQueue

# Initialize storage and messaging
audit_store = AuditStore()
message_queue = MessageQueue()

# Create reports directory if it doesn't exist
os.makedirs("reports", exist_ok=True)

# Get all .sol contract files from contracts/
contract_folder = "contracts"
contract_files = [f for f in os.listdir(contract_folder) if f.endswith(".sol")]

# Agents to run
agents = [
    CodeParserAgent(),
    ReentrancyAgent(),
    IntegerOverflowAgent(),
    AccessControlAgent(),
    GeneralStaticAnalyzerAgent(),
    TestCaseGeneratorAgent(),
    AnnotatedSummaryAgent(),
    SlitherAgent(),
    ComplianceCoordinatorAgent()
]

# Process each contract
for filename in contract_files:
    path = os.path.join(contract_folder, filename)
    with open(path, "r") as f:
        contract_code = f.read()

    # Create contract ID and store
    contract_id = audit_store.generate_contract_id()

    all_findings = []

    for agent in agents:
        findings = agent.run(contract_code)
        audit_store.save_result(contract_id, agent.name, findings)
        all_findings.append((agent.name, findings))

    # Print to console
    print(f"\n🧾 Audit completed for: {filename} (Contract ID: {contract_id})")
    print("=========================================")
    for agent_name, issues in all_findings:
        print(f"\n🔍 {agent_name}")
        for issue in issues:
            print(f" - [{issue['type']}] {issue['message']}")

    # Save Markdown report
    report_path = os.path.join("reports", f"{filename}_report.md")
    with open(report_path, "w") as report:
        report.write(f"# Audit Report: {filename}\n\n")
        report.write(f"**Contract ID:** {contract_id}\n\n")
        for agent_name, issues in all_findings:
            report.write(f"## 🔍 {agent_name}\n")
            for issue in issues:
                report.write(f"- **{issue['type']}**: {issue['message']}\n")
                if issue.get("annotated_code"):
                    report.write("\n### 📄 Annotated Code\n```solidity\n")
                    report.write(issue["annotated_code"] + "\n```\n")
                if issue.get("points"):
                    report.write("\n### 🧠 Summary Points\n")
                    for pt in issue["points"]:
                        report.write(f"- {pt}\n")
            report.write("\n")

print("\n✅ All contracts audited. Reports saved to `reports/`.\n")
