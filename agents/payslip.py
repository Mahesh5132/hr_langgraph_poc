### --- hr_langgraph_poc/agents/payslip.py ---
def payslip_node(state):
    employee_id = state.get("employee_id")
    month = state.get("month", "June")
    # Simulated salary lookup
    return {"response": f"Payslip for {employee_id} for {month} is ₹40,000"}


'''🔧 1. Payslip Agent – Industry-Ready Goals
We'll upgrade it to:

✅ Pull actual attendance & leave data

✅ Apply salary policies (basic, HRA, deductions: PF, ESIC, TDS)

✅ Generate PDF payslips with branding

✅ Maintain audit trail for compliance

Suggested Roadmap:
Define Salary Structure Model (Basic, HRA, Allowances, Gross, Net)

Add Leave Deduction Rules (LOP, partial month)

Add Tax Logic:

Fixed slabs for demo (can be read from config)

Include PF, ESIC, Professional Tax

PDF Generation using reportlab or weasyprint

Secure Storage + Distribution (Mocked for now: write to /tmp)


Your Payslip Agent has been upgraded to an industry-level version with the following features:

🔍 Key Enhancements:
MySQL Attendance Fetching – Dynamically pulls present days for the employee.

Salary Computation – Calculates gross and net salary based on attendance.

Standard Deductions – PF, ESIC, and TDS are applied using real-world formulas.

Structured Output – Payslip includes detailed breakdown.

⚙️ What You Need to Do:
Ensure a MySQL database hr_db with a table:

sql
Copy
Edit
CREATE TABLE attendance (
  id INT AUTO_INCREMENT PRIMARY KEY,
  employee_id VARCHAR(20),
  date DATE,
  status ENUM('Present', 'Absent', 'Leave')
);
Update database credentials in the code:

python
Copy
Edit
db = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_pass",
    database="hr_db"
)

✅ Payslip Agent has been enhanced with:

📄 PDF Generation – Using fpdf, a professional payslip PDF is created with salary and deductions.

📧 Auto Email – Sends the payslip to the employee’s email using SMTP (Gmail SMTP setup shown).

🛠️ Setup Notes:
Add employee email in the input state like:

python
Copy
Edit
{
  "employee_id": "E123",
  "employee_email": "employee@example.com",
  "month": "June"
}
Update these in the code:

python
Copy
Edit
sender_email = "your_email@example.com"
sender_password = "your_email_password"
'''

### --- hr_langgraph_poc/agents/payslip.py ---
import mysql.connector
from datetime import datetime
from decimal import Decimal
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# Constants (mocked, usually configurable or stored in DB)
PF_PERCENT = Decimal("0.12")  # 12%
ESIC_PERCENT = Decimal("0.0075")
TDS_PERCENT = Decimal("0.10")
BASE_SALARY = Decimal("50000.00")
WORKING_DAYS = 30

def fetch_attendance(employee_id, month):
    db = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_pass",
        database="hr_db"
    )
    cursor = db.cursor(dictionary=True)
    query = f"""
        SELECT COUNT(*) as present_days
        FROM attendance
        WHERE employee_id = %s AND MONTH(date) = %s AND status = 'Present'
    """
    cursor.execute(query, (employee_id, datetime.strptime(month, "%B").month))
    result = cursor.fetchone()
    db.close()
    return result['present_days'] if result else 0

def compute_deductions(gross_salary):
    pf = gross_salary * PF_PERCENT
    esic = gross_salary * ESIC_PERCENT
    tds = gross_salary * TDS_PERCENT
    return pf, esic, tds

def generate_pdf_payslip(employee_id, month, present_days, gross_salary, pf, esic, tds, net_salary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Payslip for {month}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Employee ID: {employee_id}", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Present Days: {present_days}", ln=True)
    pdf.cell(200, 10, txt=f"Gross Salary: ₹{gross_salary:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"PF Deduction: ₹{pf:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"ESIC Deduction: ₹{esic:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"TDS Deduction: ₹{tds:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Net Salary: ₹{net_salary:.2f}", ln=True)

    filename = f"/tmp/payslip_{employee_id}_{month}.pdf"
    pdf.output(filename)
    return filename

def send_email_with_payslip(employee_email, pdf_path):
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = employee_email
    msg['Subject'] = "Your Monthly Payslip"
    msg.attach(MIMEText("Please find your payslip attached.", 'plain'))

    with open(pdf_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=pdf_path.split("/")[-1])
        part['Content-Disposition'] = f'attachment; filename="{pdf_path.split("/")[-1]}"'
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

def payslip_node(state):
    employee_id = state.get("employee_id")
    employee_email = state.get("employee_email")  # must be included in state
    month = state.get("month", datetime.now().strftime("%B"))

    present_days = fetch_attendance(employee_id, month)
    daily_salary = BASE_SALARY / WORKING_DAYS
    gross_salary = daily_salary * Decimal(present_days)

    pf, esic, tds = compute_deductions(gross_salary)
    net_salary = gross_salary - pf - esic - tds

    # Text summary
    payslip = (
        f"Payslip for {month} ({employee_id}):\n"
        f"  Present Days: {present_days}\n"
        f"  Gross Salary: ₹{gross_salary:.2f}\n"
        f"  PF Deduction: ₹{pf:.2f}\n"
        f"  ESIC Deduction: ₹{esic:.2f}\n"
        f"  TDS Deduction: ₹{tds:.2f}\n"
        f"  Net Salary: ₹{net_salary:.2f}"
    )

    # PDF + Email
    pdf_path = generate_pdf_payslip(employee_id, month, present_days, gross_salary, pf, esic, tds, net_salary)
    send_email_with_payslip(employee_email, pdf_path)

    return {"response": payslip + "\n(PDF payslip sent to your email.)"}

'''| Feature                           | Status |
| --------------------------------- | ------ |
| MySQL attendance fetching         | ✅      |
| Salary + deduction computation    | ✅      |
| PDF payslip generation            | ✅      |
| Auto email of payslip (SMTP)      | ✅      |
| LangGraph node-style input/output | ✅      |
'''