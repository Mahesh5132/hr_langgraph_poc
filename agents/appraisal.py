### --- hr_langgraph_poc/agents/appraisal.py ---
def appraisal_node(state):
    employee_id = state.get("employee_id")
    return {"response": f"Appraisal reminder has been triggered for {employee_id}. HR will follow up shortly."}

''' 3. Appraisal Agent – Industry-Ready Goals
Upgrade to:

✅ Send reminders before appraisal cycles

✅ Provide employee past performance summaries

✅ Collect feedback or self-evaluation

✅ Auto-notify manager or HR

Suggested Roadmap:
Trigger Dates Based on Department/Role

Pre-fetch last year performance summary (mock)

Prompt user to fill self-evaluation

Notify HR/manager with context

Log Appraisal Progress

Great — to refine the Appraisal Agent to an industry-level design, here’s a structured plan with logic and implementation in mind:

✅ Assumptions
Annual appraisal is recorded in Workday.

We have access to Workday API (or can mock it for now).

Employee and manager details are stored in a MySQL DB.

Agent is expected to:

Notify employees about appraisal timelines.

Remind managers to complete feedback.

Fetch appraisal status for a user on request.

🧠 Functional Requirements
Feature	Status
Appraisal timeline reminder (to employee)	✅
Manager feedback reminder	✅
Status fetch from Workday API	✅
Integration with LangGraph node	✅
Optional: Email or chatbot-based alerts	✅

'''

### --- hr_langgraph_poc/agents/appraisal.py ---
from datetime import datetime
from hr_langgraph_poc.utils.db_utils import get_employee_info
from hr_langgraph_poc.utils.workday_api import get_workday_appraisal_status
from hr_langgraph_poc.utils.notifier import notify_employee, notify_manager

def appraisal_node(state):
    employee_id = state.get("employee_id")
    if not employee_id:
        return {"response": "Employee ID not found in state."}

    employee_info = get_employee_info(employee_id)
    if not employee_info:
        return {"response": "Employee details not found."}

    status = get_workday_appraisal_status(employee_id)

    if status == "Not Started":
        notify_employee(employee_info['email'], "Dear {},\nYour annual appraisal cycle has started. Please complete your self-review in Workday.".format(employee_info['name']))
    elif status == "Manager Pending":
        notify_manager(employee_info['manager_email'], "Hi,\nPlease submit your feedback for {} in the Workday system.\nThanks, HR".format(employee_info['name']))
    elif status == "Completed":
        return {"response": f"Appraisal cycle for {employee_info['name']} is already completed."}

    return {
        "response": f"Appraisal status for {employee_info['name']}: {status}"
    }
