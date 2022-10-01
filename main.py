from fastapi import FastAPI
import pyodbc

# database settings
driver = "ODBC Driver 17 for SQL Server"
server = "servername"
db = "dbname"
user = "username"
password = "password"

conn_str = (
    f"Driver={{{driver}}};"
    f"Server={server};"
    f"Database={db};"
    f"UID={user};"
    f"PWD={password};"
)

# get data from database with given query
def get_data(query):
    conn = pyodbc.connect(conn_str)
    cur = conn.cursor()

    cur.execute(query)
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()

    return r

# FastAPI starts
app = FastAPI()

# get all employees
@app.get('/')
async def get_employees():
    return get_data("SELECT * FROM employees")

# get employee
@app.get('/{id}/')
async def get_employees(id):
    return get_data(f"SELECT * FROM employees where employee_id={id}")
