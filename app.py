from flask import Flask, render_template, request, jsonify
import psycopg2
import csv
import io
import os
from datetime import datetime
from categorizer import categorize_transaction
from db import get_connection, init_db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400

    try:
        stream = io.StringIO(file.stream.read().decode("UTF-8"))
        reader = csv.DictReader(stream)

        transactions = []
        for row in reader:
            # Flexible: handles common bank CSV column names
            date = row.get('Date') or row.get('date') or row.get('DATE')
            description = row.get('Description') or row.get('description') or row.get('Narration') or row.get('DESCRIPTION')
            amount = row.get('Amount') or row.get('amount') or row.get('Debit') or row.get('AMOUNT')

            if not date or not description or not amount:
                continue

            try:
                amount = float(str(amount).replace(',', '').replace('₹', '').replace('$', '').strip())
            except ValueError:
                continue

            category = categorize_transaction(description)

            transactions.append({
                'date': date,
                'description': description,
                'amount': abs(amount),
                'category': category
            })

        # Save to DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions")  # Clear old data for demo

        for t in transactions:
            cursor.execute(
                "INSERT INTO transactions (date, description, amount, category) VALUES (%s, %s, %s, %s)",
                (t['date'], t['description'], t['amount'], t['category'])
            )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'count': len(transactions),
            'transactions': transactions[:5]  # Preview first 5
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, description, amount, category FROM transactions ORDER BY date DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        transactions = [
            {'date': r[0], 'description': r[1], 'amount': float(r[2]), 'category': r[3]}
            for r in rows
        ]
        return jsonify(transactions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/summary', methods=['GET'])
def get_summary():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM transactions
            GROUP BY category
            ORDER BY total DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        summary = [
            {'category': r[0], 'total': float(r[1]), 'count': int(r[2])}
            for r in rows
        ]
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
