### --- hr_langgraph_poc/agents/appraisal.py ---
def appraisal_node(state):
    employee_id = state.get("employee_id")
    return {"response": f"Appraisal reminder has been triggered for {employee_id}. HR will follow up shortly."}