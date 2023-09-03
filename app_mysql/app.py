from flask import Flask, render_template, request, jsonify
import pymysql
from pymysql.constants import CLIENT

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'db': 'project',
    'user': 'root',
    'password': 'root',
    'cursorclass': pymysql.cursors.DictCursor,
    'client_flag': CLIENT.MULTI_STATEMENTS
}

def get_database_connection():
    try:
        conn = pymysql.connect(**db_config)
        return conn
    except pymysql.Error as e:
        print("Error de conexión a la base de datos:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_student_data():
    dni = request.args.get('dni', '')
    
    conn = get_database_connection()
    if conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM estudiante WHERE dni = '{dni}';"

        print("Query: ", query)
        
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        
        except pymysql.Error as e:
            return str(e)
        
        conn.close()
        return jsonify(data)
    
    return "Error de conexión a la base de datos."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
