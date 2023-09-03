from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

db_config = {
    'dbname': 'project',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

def get_database_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.Error as e:
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

        #print("Consulta: ", query)

        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    
    return "Error de conexión a la base de datos."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
