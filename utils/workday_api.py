import random

def get_workday_appraisal_status(employee_id: str) -> str:
    # Dummy mock of Workday status check
    statuses = ["Not Started", "In Progress", "Manager Pending", "Completed"]
    return random.choice(statuses)

'''# Example (with requests)
# response = requests.get(f"https://api.workday.com/appraisal/{employee_id}", headers=headers)
# return response.json()["status"]
'''