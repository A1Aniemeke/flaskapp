from flask import Flask, render_template, jsonify
import pyodbc
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    conn = None
    cursor = None
    try:
        # Establish database connection
        conn = pyodbc.connect(
            'Driver={ODBC Driver 18 for SQL Server};'
            'Server=tcp:bdat1004-group4.database.windows.net,1433;'
            'Database=bdat1004group4;'
            'Uid=bdat1004-group4;'
            'Pwd=Programming4$;'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
        cursor = conn.cursor()

        # Execute a query
        query = "SELECT * FROM users"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Process rows into a list of dictionaries
        data = []
        for row in rows:
            data.append({
                'user_id': row[0],
                'age': row[1],
                'gender': row[2],
                'occupation': row[3],
                'zip_code': row[4],
            })

        # Render HTML template and pass data
        return render_template('index.html', data=data)

    except pyodbc.Error as e:
        return f"Error: {str(e)}", 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/chart-data', methods=['GET'])
def chart_data():
    conn = None
    try:
        conn = pyodbc.connect(
            'Driver={ODBC Driver 18 for SQL Server};'
            'Server=tcp:bdat1004-group4.database.windows.net,1433;'
            'Database=bdat1004group4;'
            'Uid=bdat1004-group4;'
            'Pwd=Programming4$;'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
        query = "SELECT occupation, COUNT(*) as count FROM users GROUP BY occupation"
        df = pd.read_sql(query, conn)

        # Return data as JSON
        return df.to_json(orient='records'), 200

    except pyodbc.Error as e:
        return f"Error: {str(e)}", 500

    finally:
        if conn:
            conn.close()

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
