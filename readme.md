# ACTOR

**ACTOR** (*Agent-based Co-auditing, Testing, Optimization & Remediation*) is a human-in-the-loop, multi-agent system for smart contract vulnerability detection, test generation, and cooperative auditing. Combining autonomous agents with expert human validation, it delivers rigorous security auditing for Solidity smart contracts.

---

## 🔍 Key Features

- 🧠 **Multi-Agent Architecture** – Specialized agents detect vulnerabilities such as reentrancy, integer overflows, access control issues, and more.
- 📚 **LLM-Style Reasoning** – Simulated large language model analysis of Solidity code for vulnerability insights and context.
- 🧪 **Test Case Generation** – Automatically produces Foundry-style fuzz tests for detected issues.
- 🧑‍⚖️ **Human-in-the-Loop Validation** – Allows manual confirmation or rejection of vulnerabilities for higher confidence.
- 📈 **Compliance Reporting** – Generates preliminary audit reports with recommended fixes and validation steps.
- 🧵 **Queue-Based Messaging** – Simulates coordination between agents using in-memory queues.

---

## 📂 Project Structure

```
.
├── agentic_audit_demo.py       # Core multi-agent engine
├── cli_demo.py                 # CLI interface for audit commands
├── contract.sol                # Example vulnerable Solidity contract
├── venv/                       # Python virtual environment
└── README.md                   # Project documentation
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
python agentic_audit_demo.py
```

### 5. Run CLI in Another Terminal

```bash
source venv/bin/activate
python cli_demo.py start
```

---

## 🧪 CLI Commands

| Command | Description |
|--------|-------------|
| `start` | Begin a new audit using the example contract |
| `review` | Show detected issues and outputs |
| `run-foundry` | Mock running a generated test script |
| `run-slither` | Mock Slither scan |
| `validate` | Mark an issue as valid or invalid |
| `list-ids` *(optional)* | Show all audited contract IDs |

Example:
```bash
python cli_demo.py review --contract-id <ID> --vulnerability reentrancy
```

---

## 🧠 Agents Involved

- **CodeParserAgent** – Parses Solidity structure
- **ReentrancyAgent** – Detects reentrancy issues
- **IntegerOverflowAgent** – Checks for overflows/underflows
- **AccessControlAgent** – Flags missing access checks
- **GeneralStaticAnalyzerAgent** – Finds other static issues
- **TestCaseGeneratorAgent** – Creates Foundry-style tests
- **ComplianceCoordinatorAgent** – Gathers all outputs and produces a summary

---

## 🛡️ Example Vulnerability: `contract.sol`

```solidity
(bool success, ) = msg.sender.call{value: amount}("");
require(success, "Transfer failed");
balances[msg.sender] = 0;
```

This reentrancy issue is caught by `ReentrancyAgent`, and a test case is generated automatically.

---

## 📌 Future Improvements

- Integrate real LLM APIs (e.g., GPT, Claude, Grok)
- Use real static analysis tools (Slither, Mythril)
- Add web UI for co-auditing visualization
- Store audit history in a database (e.g., MongoDB)
- Export PDF audit reports

---

## 🧑‍💻 Author

Developed by **Anik Tahabilder**  
PhD Student | Blockchain Researcher | Smart Contract Security Analyst

---

## 📜 License

This project is licensed under the MIT License.