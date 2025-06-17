### --- hr_langgraph_poc/graph/hr_graph.py ---
from langgraph.graph import StateGraph
from agents.payslip import payslip_node
from agents.grievance import grievance_node
from agents.appraisal import appraisal_node

builder = StateGraph()

builder.add_node("Payslip", payslip_node)
builder.add_node("Grievance", grievance_node)
builder.add_node("Appraisal", appraisal_node)

builder.set_conditional_entry_point(lambda state: state["intent"], {
    "Payslip": "Payslip",
    "Grievance": "Grievance",
    "Appraisal": "Appraisal",
})

graph = builder.compile()