from flask import Flask
app = Flask(__name__)

@app.route('/')
def func():
    return 'do something'

if __name__ == '__main__':
    app.debug = True
    app.run()
