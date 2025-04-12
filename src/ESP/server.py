from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def data():
    content = request.json
    print("Received data:", content)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
