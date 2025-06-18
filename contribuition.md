# 🛡️ Smart Contract Co-Audit Framework

This project introduces an agent-based, explainable, and human-in-the-loop auditing system for analyzing Ethereum smart contracts. It integrates static analysis tools (e.g., Slither) with LLMs and enables collaboration between humans and automated agents.

---

## 🎯 Key Contributions

### ✅ Contribution 1: Human-in-the-Loop Co-Audit Mechanism
We introduce an interactive co-auditing process where human users:
- Review, confirm, or question agent-generated findings
- Trigger re-analysis or request deeper explanations
- Maintain control over trust, severity, and follow-up actions

> 🤝 This fosters collaboration between agents and auditors, ensuring transparency, trust calibration, and iterative refinement of audit insights.

---

### ✅ Contribution 2: LLM-Augmented Interpretability Layer
We integrate large language models (LLMs) to automatically:
- Generate plain-language summaries of contracts
- Annotate source code with inline comments
- Explain detected vulnerabilities in a developer-friendly format

> 🧠 This bridges the usability gap between raw static analysis output and practical developer understanding, improving audit clarity and reducing misinterpretation.

---

### ✅ Contribution 3: Modular Agent-Based Audit Framework
We propose a modular audit architecture where each component (e.g., vulnerability scanner, explainer, annotator) is implemented as an independent agent. This enables:
- Plug-and-play extensibility
- Task-specific processing (e.g., line-by-line analysis, summarization)
- Parallel or sequential orchestration of audit workflows

> 🆚 Compared to traditional monolithic audit tools like Slither or Mythril, our agent-based design offers enhanced flexibility, scalability, and customizability.

---

## 📊 Evaluation Metrics

| **Category**           | **Metric**                                              | **Purpose**                                                                 | **Applies To**                          |
|------------------------|----------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------|
| 🔍 Accuracy            | Vulnerability Detection Rate (%)                        | Measure how accurately agents detect known issues                           | Modular Agent Framework                 |
| 🧠 Interpretability    | Annotation Clarity Score (1–5 Likert scale)             | Rate how understandable LLM-generated explanations are to developers        | LLM-Augmented Layer                     |
|                        | Summary Helpfulness (%)                                 | % of users who find summaries useful in understanding contract intent       | LLM-Augmented Layer                     |
| ⏱️ Efficiency          | Audit Time per Contract (seconds)                       | Measure total runtime of the full co-audit pipeline                         | Entire System                           |
| 🤝 Human Interaction  | User Correction Rate (%)                                 | % of vulnerabilities manually revised/confirmed by the user                 | Human-in-the-Loop Co-Audit              |
|                        | Reanalysis Trigger Count per Session                    | Number of times users request additional explanation or rerun an agent      | Human-in-the-Loop Co-Audit              |
| 🔄 Usability           | User Trust Rating (1–5 scale)                           | Measures how much users trust the agent findings                            | Human-in-the-Loop + LLM Layer           |
|                        | Modularity Score (agent plug/reuse ratio)              | Evaluate how easily components can be added, removed, or reused             | Modular Agent Framework                 |
| 🧪 Robustness          | Error Recovery Rate (%)                                 | % of times system suggests valid fixes after Slither or LLM failures        | Debug Feedback Layer (SlitherAgent etc.)|

---

> 🧩 The co-audit system aims to blend automation and oversight — not only catching bugs but also building trust in the tools that detect them.
