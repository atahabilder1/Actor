# core/audit_store.py

class AuditStore:
    def __init__(self):
        self.results = {}
        self.contract_id_counter = 1

    def save_result(self, contract_id, agent_name, issues):
        if contract_id not in self.results:
            self.results[contract_id] = {}
        self.results[contract_id][agent_name] = issues

    def get_results(self, contract_id):
        return self.results.get(contract_id, {})

    def generate_contract_id(self):
        cid = f"C{self.contract_id_counter:03}"
        self.contract_id_counter += 1
        return cid
