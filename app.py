from flask import Flask, render_template, request
import psycopg2
import time

app = Flask(__name__)

# Função para obter conexão com o banco de dados
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="pdv",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432",
        )
        return conn
    except psycopg2.OperationalError as e:
        print("Database connection failed. Retrying in 5 seconds...")
        time.sleep(5)
        return get_db_connection()

@app.route('/', methods=['GET', 'POST'])
def index():
    consulta_resultado = None
    colunas = None
    erro = None

    if request.method == 'POST':
        comando_sql = request.form['comandoSQL']
        conn = get_db_connection()

        cursor = conn.cursor()
        try:
            cursor.execute(comando_sql)
            rows = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            conn.commit()
        except psycopg2.Error as e:
            erro = str(e)
            conn.rollback()
            rows = []
        finally:
            cursor.close()

        consulta_resultado = rows

    return render_template('index.html', consulta_resultado=consulta_resultado, colunas=colunas, erro=erro)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
