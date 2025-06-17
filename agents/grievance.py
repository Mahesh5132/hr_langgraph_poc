### --- hr_langgraph_poc/agents/grievance.py ---
def grievance_node(state):
    issue = state.get("input")
    return {"response": f"Thank you for raising your concern. We will address the issue: '{issue}' soon."}