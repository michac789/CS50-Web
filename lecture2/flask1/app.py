"""
Flask 1: Jinja2 Conditional & Loop

- Use {{url_for('func')}} anchor tag to link
- Turn on debug mode when run app
- Implementing 'get' request
- Jinja2 conditional (if, elif, else)
- Jinja2 loop (for)
"""

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/parity')
def parity():
    input = False
    number = request.args.get("num", "0.5")
    number = float(number)
    if number != 0.5: input = True
    return render_template("parity.html", number=number, input=input)

@app.route('/numbers')
def numbers():
    number = request.args.get("num", 0)
    numbers = [i for i in range(1, int(number) + 1)]
    return render_template("numbers.html", numbers=numbers, length=len(numbers))

if __name__ == "__main__":
    app.run(debug=True)
