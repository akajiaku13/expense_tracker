
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = "expenses.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        date TEXT NOT NULL,
                        note TEXT)''')
        conn.commit()

@app.route('/')
def dashboard():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = c.fetchall()
        c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        category_data = c.fetchall()
        total = sum(row[1] for row in category_data)
    return render_template("dashboard.html", expenses=expenses, category_data=category_data, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        note = request.form['note']
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
                      (amount, category, date, note))
            conn.commit()
        return redirect(url_for('dashboard'))
    return render_template("add.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')
