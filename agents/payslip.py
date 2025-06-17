### --- hr_langgraph_poc/agents/payslip.py ---
def payslip_node(state):
    employee_id = state.get("employee_id")
    month = state.get("month", "June")
    # Simulated salary lookup
    return {"response": f"Payslip for {employee_id} for {month} is ₹40,000"}