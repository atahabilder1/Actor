# ACTOR

**ACTOR** (*Agent-based Co-auditing, Testing, Optimization & Remediation*) is a human-in-the-loop, multi-agent system for smart contract vulnerability detection, test generation, and cooperative auditing. Combining autonomous agents with expert human validation, it delivers rigorous security auditing for Solidity smart contracts.

---

## 🔍 Key Features

- 🧠 **Multi-Agent Architecture** – Specialized agents detect vulnerabilities like reentrancy, overflows, and access control flaws.
- 🤖 **LLM-Powered Analysis** – Uses GPT to annotate code and summarize logic in plain English.
- 🧪 **Test Case Generation** – Automatically creates Foundry-style fuzz tests for each issue.
- 🧑‍⚖️ **Human-in-the-Loop Validation** – Allows manual review of issues before finalizing.
- 📊 **Markdown Audit Reports** – Saves readable reports in `reports/` folder.
- 🧵 **Queue-Based Messaging** – Agents coordinate through a simulated messaging system.
- 🛠 **Slither Integration** – Uses real static analysis to enhance vulnerability detection.

---

## 📂 Project Structure

```
.
├── agentic_audit_system.py            # Main orchestrator (now processes multiple contracts)
├── cli_demo.py                        # CLI interface for demo interaction
├── activate.sh                        # Activates Python environment
├── .env                               # Stores API key for LLM
├── LICENSE                            # MIT License
├── README.md                          # Project documentation
├── contracts/                         # Input folder for all Solidity contracts
│   └── MyContract.sol                 # Example or target smart contracts
├── reports/                           # Output folder for audit reports (.md)
├── core/                              # Core system logic
│   ├── base_agent.py
│   ├── audit_store.py
│   └── message_queue.py
└── agents/                            # Modular auditing agents
    ├── code_parser_agent.py
    ├── reentrancy_agent.py
    ├── integer_overflow_agent.py
    ├── access_control_agent.py
    ├── static_analyzer_agent.py
    ├── test_case_generator_agent.py
    ├── annotated_summary_agent.py
    ├── slither_agent.py
    └── compliance_coordinator_agent.py
```

---

## 🔄 Workflow

```text
       contracts/*.sol        📝        Multiple smart contract inputs
               │
               ▼
     +----------------------+
     | agentic_audit_system |
     +----------+-----------+
                │
   +------------+-------------+
   | Agents (run sequentially)|
   +--------------------------+
   | - CodeParserAgent        |
   | - ReentrancyAgent        |
   | - IntegerOverflowAgent   |
   | - AccessControlAgent     |
   | - StaticAnalyzerAgent    |
   | - TestCaseGeneratorAgent |
   | - AnnotatedSummaryAgent  |
   | - SlitherAgent           |
   | - ComplianceCoordinator  |
   +--------------------------+
                │
                ▼
        reports/<contract>_report.md
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

```bash
pip install openai python-dotenv click
```

### 4. Add Your API Key to `.env`

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Add Contracts

Put all `.sol` files inside the `contracts/` folder.

---

### 6. Run the Audit System

```bash
python agentic_audit_system.py
```

Markdown reports will be saved to the `reports/` folder.

---

## 🧪 CLI Demo Commands (Optional)

| Command       | Description                                |
|---------------|--------------------------------------------|
| `start`       | Begin an audit using the demo contract     |
| `review`      | Show issues identified by agents           |
| `run-foundry` | Mock: simulate running a test              |
| `run-slither` | Mock: simulate static scan                 |
| `validate`    | Mark vulnerability as valid or not         |
| `list-ids`    | Show contract IDs already analyzed         |

---

## 🧠 Agents Involved

| Agent                        | Responsibility                                                    |
|-----------------------------|-------------------------------------------------------------------|
| **CodeParserAgent**         | Parses code and extracts structural information                   |
| **ReentrancyAgent**         | Detects reentrancy attack patterns                                |
| **IntegerOverflowAgent**    | Flags unsafe math (e.g., overflows, lack of SafeMath)             |
| **AccessControlAgent**      | Detects missing access checks                                     |
| **GeneralStaticAnalyzerAgent** | Flags unsafe or deprecated Solidity patterns                 |
| **TestCaseGeneratorAgent**  | Creates fuzzing tests for vulnerable functions                    |
| **AnnotatedSummaryAgent**   | Calls LLM to annotate the contract and summarize its behavior     |
| **SlitherAgent**            | Runs real Slither scan and integrates JSON results                |
| **ComplianceCoordinatorAgent** | Compiles and summarizes all findings into the final report   |

---

## 🛡️ Example Vulnerability

```solidity
function withdraw(uint amount) public {
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
    balances[msg.sender] = 0; // 🔥 Reentrancy vulnerability
}
```

This pattern is flagged by:
- ✅ `ReentrancyAgent`
- ✅ `AnnotatedSummaryAgent` (explains logic)
- ✅ `SlitherAgent` (real static analysis)
- ✅ `TestCaseGeneratorAgent` (generates a fuzz test)

---

## 📌 Planned Enhancements

- Add rich HTML/PDF report export
- Enable web dashboard for auditing visibility
- Integrate Mythril and Echidna for deeper analysis
- Support GitHub contract loading and issue triage

---

## 🧑‍💻 Author

Developed by **Anik Tahabilder**  
PhD Student | Department of Computer Science | Wayne State University

---

## 📜 License

This project is licensed under the **MIT License**.
