from flask import Flask
app = Flask(__name__)
@app.route('/checkResult', methods=['POST'])
def checkResult(idRequest):
    return correlationMap[idRequest]