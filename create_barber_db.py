import sqlite3
from datetime import datetime, timedelta

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('barber_appointments.db')
cursor = conn.cursor()

# Create appointments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone_number TEXT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    service_type TEXT NOT NULL,
    barber_name TEXT NOT NULL,
    duration_minutes INTEGER,
    price DECIMAL(10, 2),
    status TEXT DEFAULT 'scheduled',
    notes TEXT
)
''')

# Sample barber appointment data
appointments = [
    ('John Smith', '555-0101', '2025-10-20', '09:00', 'Haircut', 'Mike Johnson', 30, 25.00, 'scheduled', 'Regular customer'),
    ('Emma Davis', '555-0102', '2025-10-20', '10:00', 'Haircut & Beard Trim', 'Mike Johnson', 45, 40.00, 'scheduled', 'First time customer'),
    ('Michael Brown', '555-0103', '2025-10-20', '11:00', 'Beard Trim', 'Sarah Williams', 20, 15.00, 'scheduled', None),
    ('James Wilson', '555-0104', '2025-10-20', '14:00', 'Haircut', 'Sarah Williams', 30, 25.00, 'scheduled', 'Prefers fade cut'),
    ('Robert Taylor', '555-0105', '2025-10-20', '15:00', 'Full Service', 'Mike Johnson', 60, 55.00, 'scheduled', 'Haircut, beard trim, and hot towel'),
    ('David Martinez', '555-0106', '2025-10-21', '09:30', 'Haircut', 'Sarah Williams', 30, 25.00, 'scheduled', None),
    ('Christopher Lee', '555-0107', '2025-10-21', '10:30', 'Kids Haircut', 'Mike Johnson', 20, 18.00, 'scheduled', 'Age 8, bring booster seat'),
    ('Daniel Anderson', '555-0108', '2025-10-21', '11:30', 'Beard Trim', 'Sarah Williams', 20, 15.00, 'scheduled', None),
    ('Matthew Thomas', '555-0109', '2025-10-21', '13:00', 'Haircut & Shave', 'Mike Johnson', 50, 45.00, 'scheduled', 'Hot towel shave'),
    ('Anthony Garcia', '555-0110', '2025-10-21', '14:30', 'Haircut', 'Sarah Williams', 30, 25.00, 'scheduled', None),
    ('Paul Martinez', '555-0111', '2025-10-22', '09:00', 'Full Service', 'Mike Johnson', 60, 55.00, 'scheduled', 'Regular Wednesday appointment'),
    ('Mark Robinson', '555-0112', '2025-10-22', '10:30', 'Haircut', 'Sarah Williams', 30, 25.00, 'scheduled', None),
    ('Steven Clark', '555-0113', '2025-10-22', '11:30', 'Beard Trim', 'Mike Johnson', 20, 15.00, 'scheduled', None),
    ('Kevin Rodriguez', '555-0114', '2025-10-22', '14:00', 'Haircut', 'Sarah Williams', 30, 25.00, 'completed', 'Tipped $5'),
    ('Brian Lewis', '555-0115', '2025-10-22', '15:00', 'Kids Haircut', 'Mike Johnson', 20, 18.00, 'completed', 'Age 6'),
    ('George Walker', '555-0116', '2025-10-23', '09:00', 'Haircut & Beard Trim', 'Mike Johnson', 45, 40.00, 'scheduled', None),
    ('Kenneth Hall', '555-0117', '2025-10-23', '10:30', 'Haircut', 'Sarah Williams', 30, 25.00, 'scheduled', None),
    ('Joshua Allen', '555-0118', '2025-10-23', '11:30', 'Shave', 'Mike Johnson', 25, 20.00, 'scheduled', 'Straight razor shave'),
    ('Ryan Young', '555-0119', '2025-10-23', '14:00', 'Haircut', 'Sarah Williams', 30, 25.00, 'scheduled', None),
    ('Jacob King', '555-0120', '2025-10-23', '15:30', 'Full Service', 'Mike Johnson', 60, 55.00, 'scheduled', 'Monthly appointment'),
]

# Insert sample data
cursor.executemany('''
INSERT INTO appointments (customer_name, phone_number, appointment_date, appointment_time,
                         service_type, barber_name, duration_minutes, price, status, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', appointments)

# Commit changes
conn.commit()

# Display summary
cursor.execute('SELECT COUNT(*) FROM appointments')
count = cursor.fetchone()[0]
print(f"Database created successfully!")
print(f"Total appointments inserted: {count}")

# Show sample data
print("\nSample appointments:")
cursor.execute('''
SELECT id, customer_name, appointment_date, appointment_time, service_type, barber_name, price
FROM appointments
LIMIT 5
''')
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Customer: {row[1]}, Date: {row[2]}, Time: {row[3]}, Service: {row[4]}, Barber: {row[5]}, Price: ${row[6]}")

# Close connection
conn.close()
print("\nDatabase file: barber_appointments.db")
