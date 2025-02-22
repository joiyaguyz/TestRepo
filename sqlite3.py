import sqlite3

def connect_db():
    return sqlite3.connect("example.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        department_id INTEGER,
                        FOREIGN KEY (department_id) REFERENCES departments(id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS departments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

def insert_user(name, age, department_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, department_id) VALUES (?, ?, ?)", (name, age, department_id))
    conn.commit()
    conn.close()

def insert_department(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user(user_id, new_name, new_age):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (new_name, new_age, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_average_age():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(age) FROM users")
    avg_age = cursor.fetchone()[0]
    conn.close()
    return avg_age

def get_users_with_departments():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT users.id, users.name, users.age, departments.name AS department_name
                      FROM users
                      LEFT JOIN departments ON users.department_id = departments.id''')
    result = cursor.fetchall()
    conn.close()
    return result

def main():
    create_tables()
    insert_department("HR")
    insert_department("Engineering")
    insert_user("Alice", 25, 1)
    insert_user("Bob", 30, 2)
    insert_user("Charlie", 28, 1)
    
    print("Users before update:", get_users())
    update_user(1, "Alice Johnson", 26)
    print("Users after update:", get_users())
    delete_user(2)
    print("Users after deletion:", get_users())
    
    print("Average age of users:", get_average_age())
    print("Users with departments:", get_users_with_departments())

if __name__ == "__main__":
    main()
