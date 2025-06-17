# agentic_audit_system.py

from agents.code_parser_agent import CodeParserAgent
from agents.reentrancy_agent import ReentrancyAgent
from agents.integer_overflow_agent import IntegerOverflowAgent
from agents.access_control_agent import AccessControlAgent
from agents.static_analyzer_agent import GeneralStaticAnalyzerAgent
from agents.test_case_generator_agent import TestCaseGeneratorAgent
from agents.annotated_summary_agent import AnnotatedSummaryAgent
from agents.compliance_coordinator_agent import ComplianceCoordinatorAgent

from core.audit_store import AuditStore
from core.message_queue import MessageQueue

# Initialize storage and messaging
audit_store = AuditStore()
message_queue = MessageQueue()

# Load example contract
with open("contract.sol", "r") as f:
    contract_code = f.read()

# Generate a new contract ID
contract_id = audit_store.generate_contract_id()

# Instantiate agents
agents = [
    CodeParserAgent(),
    ReentrancyAgent(),
    IntegerOverflowAgent(),
    AccessControlAgent(),
    GeneralStaticAnalyzerAgent(),
    TestCaseGeneratorAgent(),
    AnnotatedSummaryAgent(),                # ✅ Newly added annotation agent
    ComplianceCoordinatorAgent()
]

# Run agents
for agent in agents:
    findings = agent.run(contract_code)
    audit_store.save_result(contract_id, agent.name, findings)

# Output summary
print(f"\n🧾 Audit completed for contract ID: {contract_id}")
print("=====================================")
results = audit_store.get_results(contract_id)
for agent_name, issues in results.items():
    print(f"\n🔍 {agent_name}")
    for issue in issues:
        print(f" - [{issue['type']}] {issue['message']}")
        if issue.get("annotated_code"):
            print("\n📄 Annotated Code:\n" + issue["annotated_code"])
        if issue.get("points"):
            print("\n🧠 Summary Points:")
            for pt in issue["points"]:
                print(f"   • {pt}")
