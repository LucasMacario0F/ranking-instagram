from flask import Flask, render_template
import json
import csv

app = Flask(__name__)

@app.route('/')
def home():
    try:
        with open('data/rankings.json', 'r', encoding='utf-8') as f:
            rankings = json.load(f)
    except:
        rankings = []
    
    return render_template('index.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True)