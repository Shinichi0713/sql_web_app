from flask import Flask, request, render_template
import sqlite3
import pandas as pd
import os
os.chdir(os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('chinook.db')
        try:
            df = pd.read_sql_query(query, conn)
            result = df.to_html()
        except Exception as e:
            result = str(e)
        return render_template(r'C:\Users\yoshinaga\Documents\Python Scripts\ForTrial\4_application\sql_web_app\index.html', result=result)
    return render_template(r'C:\Users\yoshinaga\Documents\Python Scripts\ForTrial\4_application\sql_web_app\index.html', result="")

if __name__ == "__main__":
    app.run()