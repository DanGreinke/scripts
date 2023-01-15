from flask import Flask, request

app = Flask(__name__)


#curl http://localhost:5000/addition -F "data=1,2,3"
@app.route('/addition', methods=['POST','GET'])
def addition():
    try:
        request.method == 'POST'
        input_data = request.form['data'].split(',')
        int_list = [eval(i) for i in input_data]
        return str(sum(int_list))
    except:
        return "Please input a comma separated list of integers (e.g. 1,2,3)"

app.run()