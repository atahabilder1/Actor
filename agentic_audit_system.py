import os
from core.report_generator import generate_report
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

# Initialize
audit_store = AuditStore()
message_queue = MessageQueue()

# Paths
CONTRACT_FOLDER = "contracts"
REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Define agents
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

# Audit all contracts
contract_files = [f for f in os.listdir(CONTRACT_FOLDER) if f.endswith(".sol")]

for filename in contract_files:
    print(f"\n🔧 Auditing: {filename}")
    path = os.path.join(CONTRACT_FOLDER, filename)

    with open(path, "r") as f:
        contract_code = f.read()

    contract_id = audit_store.generate_contract_id()
    all_findings = []

    for agent in agents:
        print(f"  ➤ Running {agent.name}...")
        try:
            findings = agent.run(contract_code)
        except Exception as e:
            error_msg = str(e)
            print(f"    ❌ {agent.name} failed: {error_msg}")
            findings = [{
                "type": "AgentError",
                "message": f"{agent.name} encountered an error and did not complete.",
                "line": "—",
                "details": error_msg
            }]
        audit_store.save_result(contract_id, agent.name, findings)
        all_findings.append((agent.name, findings))

    # Generate Markdown report
    report_path = os.path.join(REPORT_FOLDER, f"{filename}_report.md")
    # generate_report(contract_id, filename, all_findings, report_path)
    generate_report(contract_id, dict(all_findings), REPORT_FOLDER, filename)


print("\n✅ All contracts audited. Reports saved to `reports/`.\n")
