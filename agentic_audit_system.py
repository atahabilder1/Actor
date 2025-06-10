```python
# agentic_audit_demo.py
# Simplified multi-agent system for vulnerability detection demo

import json
import time
import queue
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock Solidity contract (same as provided)
CONTRACT_CODE = """
pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint) balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        balances[msg.sender] = 0;
    }
}
"""

# In-memory storage (replaces MongoDB)
audit_store = {}

# In-memory message queue (replaces Redis)
message_queue = queue.Queue()
queue_lock = threading.Lock()

# Mock Grok 3 API (simulates LLM responses)
def mock_grok_api(prompt, input_data):
    if "parse Solidity code" in prompt:
        return json.dumps({
            "structure": {
                "functions": [{"name": "withdraw", "payable": True, "calls": ["msg.sender.call"], "state_updates": ["balances[msg.sender]"]}],
                "variables": [{"name": "balances", "type": "mapping(address => uint)"}]
            },
            "notes": "External call before state update in withdraw"
        })
    elif "reentrancy detection" in prompt:
        return json.dumps([{
            "line": 5,
            "issue": "reentrancy",
            "description": "External call to msg.sender.call before updating balances[msg.sender]",
            "test_case": {
                "script": """
contract Malicious {
    Vulnerable target;
    function attack() public { target.withdraw(); }
    receive() external payable { if (address(this).balance > 0) target.withdraw(); }
}
contract TestVulnerable {
    function testReentrancy() public {
        // Deploy Vulnerable and Malicious, call attack()
    }
}
                """,
                "purpose": "Tests if withdraw allows multiple withdrawals before balance update"
            }
        }])
    elif "integer overflow" in prompt:
        return json.dumps([])
    elif "access control" in prompt:
        return json.dumps([])
    elif "general static analysis" in prompt:
        return json.dumps([{
            "line": 5,
            "issue": "unchecked_return",
            "description": "Return value of msg.sender.call not checked",
            "test_case": "Test withdraw with a failing call"
        }])
    elif "test case generator" in prompt:
        return json.dumps([{
            "script": """
contract TestVulnerable {
    function testDenialOfService() public {
        // Test if withdraw can be blocked by malicious contract
    }
}
            """,
            "description": "Tests for denial-of-service via malicious receiver"
        }])
    elif "compliance and coordination" in prompt:
        return json.dumps({
            "compliance": {"issues": ["Missing nonReentrant modifier"], "fixes": ["Add OpenZeppelin ReentrancyGuard"]},
            "report": {
                "summary": "Reentrancy detected at line 5; validate with Foundry or Slither",
                "actions": ["Run forge test --script reentrancy_test.sol", "Run slither contract.sol"]
            }
        })
    return json.dumps({})

# Agent base class
class Agent:
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt
        self.logger = logging.getLogger(f"Agent_{name}")

    def process(self, contract_id, input_data):
        self.logger.info(f"Processing contract {contract_id}")
        response = mock_grok_api(self.prompt, input_data)
        output = json.loads(response)
        with queue_lock:
            audit_store.setdefault(contract_id, {})[f"{self.name}_output"] = output
        message_queue.put({"channel": f"{self.name}_output", "data": {"contract_id": contract_id, "output": output}})
        self.converse(contract_id, output)

    def converse(self, contract_id, output):
        pass  # Overridden by specific agents

# Agent implementations
class CodeParserAgent(Agent):
    def __init__(self):
        super().__init__("parser", """
You are a Solidity code parser. Parse the provided code into a JSON structure with functions, variables, and external calls. Note unusual patterns.
Output: {"structure": {...}, "notes": str}
        """)

class ReentrancyAgent(Agent):
    def __init__(self):
        super().__init__("reentrancy", """
You are a reentrancy detection expert. Analyze the provided JSON structure for external calls before state updates.
Output: [{"line": int, "issue": "reentrancy", "description": str, "test_case": {"script": str, "purpose": str}}]
        """)

    def converse(self, contract_id, output):
        if output:
            self.logger.info("Found reentrancy; asking General Static Analyzer to check related issues")
            message_queue.put({
                "channel": "general_static_request",
                "data": {
                    "contract_id": contract_id,
                    "from": "reentrancy",
                    "request": "Check for unchecked return values in external calls"
                }
            })

class IntegerOverflowAgent(Agent):
    def __init__(self):
        super().__init__("integer_overflow", """
You are an integer overflow detection expert. Analyze the JSON structure for unchecked arithmetic.
Output: [{"line": int, "issue": "integer_overflow", "description": str, "test_case": {"script": str, "purpose": str}}]
        """)

class AccessControlAgent(Agent):
    def __init__(self):
        super().__init__("access_control", """
You are an access control expert. Analyze the JSON structure for missing onlyOwner or public functions.
Output: [{"line": int, "issue": "access_control", "description": str, "test_case": {"script": str, "purpose": str}}]
        """)

class GeneralStaticAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__("general_static", """
You are a general static analysis expert. Analyze the JSON structure for vulnerabilities like unchecked return values or timestamp dependence, excluding reentrancy, integer overflow, and access control.
Output: [{"line": int, "issue": str, "description": str, "test_case": str}]
        """)

    def converse(self, contract_id, output):
        # Simulate listening for requests
        while not message_queue.empty():
            message = message_queue.get()
            if message["channel"] == "general_static_request":
                data = message["data"]
                if data["from"] == "reentrancy":
                    self.logger.info("Received reentrancy request; re-analyzing")
                    self.process(contract_id, data["request"])

class TestCaseGeneratorAgent(Agent):
    def __init__(self):
        super().__init__("test_case", """
You are a test case generator. Generate Foundry test scripts for runtime issues like denial of service, based on the JSON structure and vulnerability outputs.
Output: [{"script": str, "description": str}]
        """)

class ComplianceCoordinatorAgent(Agent):
    def __init__(self):
        super().__init__("compliance_coordinator", """
You are a compliance and coordination expert. Check the contract for ERC standards and best practices. Collect outputs from all agents, resolve conflicts, and generate a preliminary report with validation steps.
Output: {"compliance": {"issues": [str], "fixes": [str]}, "report": {"summary": str, "actions": [str]}}
        """)

    def process(self, contract_id, input_data):
        # Wait for all agent outputs
        required = ['parser', 'reentrancy', 'integer_overflow', 'access_control', 'general_static', 'test_case']
        outputs = {}
        start_time = time.time()
        while len(outputs) < len(required) and time.time() - start_time < 10:
            with queue_lock:
                if contract_id in audit_store:
                    for agent in required:
                        if f"{agent}_output" in audit_store[contract_id] and agent not in outputs:
                            outputs[agent] = audit_store[contract_id][f"{agent}_output"]
            time.sleep(0.1)
        super().process(contract_id, outputs)

# Orchestrator
def start_audit(contract_id):
    logger.info(f"Starting audit for contract {contract_id}")
    with queue_lock:
        audit_store[contract_id] = {"contract": CONTRACT_CODE}
    message_queue.put({"channel": "contract_input", "data": {"contract_id": contract_id, "code": CONTRACT_CODE}})

# Run agents
def run_agents():
    agents = [
        CodeParserAgent(),
        ReentrancyAgent(),
        IntegerOverflowAgent(),
        AccessControlAgent(),
        GeneralStaticAnalyzerAgent(),
        TestCaseGeneratorAgent(),
        ComplianceCoordinatorAgent()
    ]
    while True:
        try:
            message = message_queue.get(timeout=1)
            data = message["data"]
            contract_id = data["contract_id"]
            if message["channel"] == "contract_input":
                threading.Thread(target=agents[0].process, args=(contract_id, data["code"])).start()
            elif message["channel"] == "parser_output":
                for agent in agents[1:-1]:
                    threading.Thread(target=agent.process, args=(contract_id, data["output"])).start()
            elif message["channel"] in [f"{a.name}_output" for a in agents[:-1]]:
                threading.Thread(target=agents[-1].process, args=(contract_id, data["output"])).start()
        except queue.Empty:
            continue

if __name__ == "__main__":
    threading.Thread(target=run_agents, daemon=True).start()
    print("Agent system running. Use cli_demo.py to start an audit.")
```