# ACTOR

**ACTOR** (*Agent-based Co-auditing, Testing, Optimization & Remediation*) is a human-in-the-loop, multi-agent system for smart contract vulnerability detection, test generation, and cooperative auditing. Combining autonomous agents with expert human validation, it delivers rigorous security auditing for Solidity smart contracts.

---

## 🔍 Key Features

- 🧠 **Multi-Agent Architecture** – Specialized agents detect vulnerabilities such as reentrancy, integer overflows, access control issues, and more.
- 📚 **LLM-Style Reasoning** – Simulated large language model analysis of Solidity code for insights and context.
- 🧪 **Test Case Generation** – Automatically produces Foundry-style fuzz tests for detected issues.
- 🧑‍⚖️ **Human-in-the-Loop Validation** – Allows manual confirmation or rejection of vulnerabilities for higher confidence.
- 📈 **Compliance Reporting** – Generates preliminary audit reports with recommended fixes and validation steps.
- 🧵 **Queue-Based Messaging** – Simulates coordination between agents using in-memory queues.
- 🧠 **Annotated Code Summary** – Highlights key logic in Solidity code and explains behavior in plain English.

---

## 📂 Project Structure

```
.
├── agentic_audit_system.py            # Main orchestrator that coordinates all agents
├── cli_demo.py                        # CLI interface for audit commands
├── contract.sol                       # Example vulnerable Solidity contract
├── activate.sh                        # Shell script for activating the Python virtual environment
├── .env                               # Environment variables (ignored by Git)
├── .gitignore                         # Git ignore rules
├── LICENSE                            # MIT License
├── README.md                          # Project documentation
├── core/                              # Core system utilities and base agent class
│   ├── __init__.py
│   ├── base_agent.py
│   ├── audit_store.py
│   └── message_queue.py
└── agents/                            # Specialized security audit agents
    ├── __init__.py
    ├── code_parser_agent.py
    ├── reentrancy_agent.py
    ├── integer_overflow_agent.py
    ├── access_control_agent.py
    ├── static_analyzer_agent.py
    ├── test_case_generator_agent.py
    ├── annotated_summary_agent.py
    └── compliance_coordinator_agent.py
```

---

## 🔄 Workflow

```text
          +------------------------+
          |  contract.sol (input)  |
          +-----------+------------+
                      |
                      v
            +-----------------------+
            | AgenticAuditSystem.py |
            +-----------+-----------+
                        |
        +---------------+-----------------------------+
        |     Agents (run sequentially or in parallel) |
        +----------------------------------------------+
        | CodeParserAgent                              |
        | ReentrancyAgent                              |
        | IntegerOverflowAgent                         |
        | AccessControlAgent                           |
        | GeneralStaticAnalyzerAgent                   |
        | TestCaseGeneratorAgent                       |
        | AnnotatedSummaryAgent                        |
        | ComplianceCoordinatorAgent                   |
        +----------------+-----------------------------+
                         |
                         v
         +------------------------------------------+
         |        AuditStore + CLI/Report Output     |
         +------------------------------------------+
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ACTOR.git
cd ACTOR
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

No external libraries are required for the mock demo. Optional: install `click` if not available.

```bash
pip install click
```

### 4. Start Agent System

```bash
python agentic_audit_system.py
```

### 5. Run CLI in Another Terminal

```bash
source venv/bin/activate
python cli_demo.py start
```

---

## 🧪 CLI Commands

| Command       | Description                                |
|---------------|--------------------------------------------|
| `start`       | Begin a new audit using the example contract |
| `review`      | Show detected issues and outputs           |
| `run-foundry` | Mock running a generated test script       |
| `run-slither` | Mock Slither scan                          |
| `validate`    | Mark an issue as valid or invalid          |
| `list-ids`    | Show all audited contract IDs (optional)   |

**Example:**
```bash
python cli_demo.py review --contract-id C001 --vulnerability reentrancy
```

---

## 🧠 Agents Involved

| Agent                        | Role                                                                 |
|-----------------------------|----------------------------------------------------------------------|
| **CodeParserAgent**         | Parses Solidity structure, generates call graphs, and annotates code |
| **ReentrancyAgent**         | Detects reentrancy vulnerabilities                                   |
| **IntegerOverflowAgent**    | Detects integer overflows and underflows                             |
| **AccessControlAgent**      | Flags functions missing access control                               |
| **GeneralStaticAnalyzerAgent** | Detects miscellaneous static issues                              |
| **TestCaseGeneratorAgent**  | Produces Foundry-style fuzz test cases                               |
| **AnnotatedSummaryAgent**   | Adds inline comments and summarizes contract logic                   |
| **ComplianceCoordinatorAgent** | Aggregates findings and produces audit summaries                |

---

## 🛡️ Example Vulnerability: `contract.sol`

```solidity
function withdraw(uint amount) public {
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
    balances[msg.sender] = 0; // 🛑 Reentrancy risk: update should come before transfer
}
```

This reentrancy issue is detected by `ReentrancyAgent`, and a corresponding test case is generated by `TestCaseGeneratorAgent`.

---

## 📌 Future Improvements

- Integrate real LLM APIs (e.g., GPT, Claude, Grok)
- Use real static analysis tools (Slither, Mythril, Echidna)
- Add web UI for co-auditing visualization
- Store audit history in a database (e.g., MongoDB)
- Export audit reports in PDF format

---

## 🧑‍💻 Author

Developed by **Anik Tahabilder**  
PhD Student | Blockchain Researcher | Smart Contract Security Analyst

---

## 📜 License

This project is licensed under the MIT License.
