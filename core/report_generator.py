import os

def generate_report(contract_id, results, output_folder, contract_filename):
    # Ensure the report output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Define the report path
    report_path = os.path.join(output_folder, f"{contract_filename}_report.md")

    with open(report_path, "w") as f:
        # 📜 Title and Metadata
        f.write(f"# 📜 Audit Report: `{contract_filename}`\n\n")
        f.write(f"**Contract ID:** `{contract_id}`\n\n")

        # 📊 Summary Table
        f.write("## 📊 Summary Table\n\n")
        f.write("| Agent | Type | Line | Message |\n")
        f.write("|-------|------|------|---------|\n")
        for agent_name, issues in results.items():
            for issue in issues:
                line = issue.get("line", "—")
                message = issue.get("message", "").replace("\n", " ")
                issue_type = issue.get("type", "")
                f.write(f"| {agent_name} | {issue_type} | {line} | {message} |\n")
        f.write("\n---\n")

        # 🔍 Detailed Per-Agent Breakdown
        for agent_name, issues in results.items():
            f.write(f"\n## 🔍 {agent_name}\n\n")
            if not issues:
                f.write("- ✅ No issues detected.\n\n")
                continue
            for issue in issues:
                issue_type = issue.get("type", "Unknown")
                line_info = f"(Line {issue['line']})" if 'line' in issue else ""
                message = issue.get("message", "")
                f.write(f"- **[{issue_type}]** {line_info}: {message}\n")

                # Optional summary points
                if issue.get("points"):
                    f.write("\n  ### 🧠 Summary Points\n")
                    for pt in issue["points"]:
                        f.write(f"  - 💡 {pt}\n")

                # Optional annotated code
                if issue.get("annotated_code"):
                    f.write("\n  ### 📄 Annotated Code\n")
                    f.write("  ```solidity\n")
                    f.write(issue["annotated_code"])
                    f.write("\n  ```\n")
                f.write("\n")
