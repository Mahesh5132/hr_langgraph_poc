import mysql.connector

def get_employee_info(employee_id):
    db = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_pass",
        database="hr_db"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, e.name, e.email, m.email AS manager_email
        FROM employees e
        LEFT JOIN employees m ON e.manager_id = m.id
        WHERE e.id = %s
    """, (employee_id,))
    
    result = cursor.fetchone()
    db.close()
    return result
