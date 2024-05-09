# from asyncore import file_wrapper
import json, logging
from flask import Flask, render_template, request, jsonify
import requests
import psycopg2
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)

# db_params = {'host': 'localhost',
#         'database': 'soaltee',
#         'user': 'postgres',
#      'password': '1234'
#   }

db_params = {'host': os.environ['DB_HOST'],
        'database': os.environ['DB_NAME'],
        'user': os.environ['DB_USER'],
     'password': os.environ['DB_PASSWORD']
  }

rasa_host = 'soaltee_rasa'
def get_db_connection():
    conn = psycopg2.connect(**db_params)
    return conn, conn.cursor()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/parse', methods=['POST', 'GET'])
def extract():
    text = request.form.get('message')
    payload = json.dumps({"sender": "Rasa", "message": text})
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    # Configure Rasa to accept POST requests
    response = requests.request("POST", url="http://soaltee_rasa:5005/webhooks/rest/webhook", headers=headers, data=payload)

    print("Response status code:", response.status_code)
    print("Response content:", response.text)

    response = response.json()
    resp=[]
    for i in range(len(response)):
      try:
        resp.append(response[i]['text'])
      except:
        continue
    result=resp
        
    # Log the user input and response
    print(f"User input: {text}, Response: {result}")

    try:
        con, cursor = get_db_connection()
        print("Connected to database")
        data = (text, result)
        insert_query = "INSERT into bot (question, answer) VALUES (%s , %s);"
        cursor.execute(insert_query, data)
        con.commit()
        print("Done Successfully")
        cursor.close()
        con.close()
    except Exception as e:
        print(e)

    return jsonify({"response": result})

# Fetching data Function

@app.route('/fetch', methods=['GET'])
def data_fetch():
  con, cursor = get_db_connection()
  query = "SELECT * from bot;"

  cursor.execute(query)

  records = cursor.fetchall()

  column_names = [desc[0] for desc in cursor.description]
  formatted_data = [dict(zip(column_names, row)) for row in records]
  json_data = json.dumps(formatted_data)

  cursor.close()
  con.close()

  return json_data  



if __name__ == "__main__":
  app.run(host = '0.0.0.0', debug=True)