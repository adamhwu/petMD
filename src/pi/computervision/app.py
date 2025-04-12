from flask import Flask, request

app = Flask(__name__)
latest_data = {}

@app.route('/petdata', methods=['POST'])
def receive_data():
    global latest_data
    latest_data = request.json
    print("Received:", latest_data)
    return '', 200

@app.route('/')
def dashboard():
    return f"Latest data: {latest_data}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
