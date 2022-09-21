from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def receive_data():
    name = request.form['name']  # request.form returns data in dictionary form
    password = request.form['password']
    if request.method == 'POST':
        return render_template('h1.html', name=name, password=password)


if __name__ == '__main__':
    app.run(debug=True)
