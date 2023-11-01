from flask import Flask , render_template , request , jsonify
import numpy as np
import pandas as pd
import pickle

global cur_data
global cur_score
model = pickle.load(open('model.pkl' , 'rb'))

ranklist = {
    "nit raipur":66 
}
institute = ""

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/updated' )
def update():
    try:
        c_name = cur_data
        rank = cur_score

        if c_name is not None and rank is not None:
            ranklist[c_name] = int(rank)  # Parse rank as an integer
            return jsonify({"message": "Ranking updated successfully"})
        else:
            return jsonify({"error": "Invalid data. Please provide 'institute' and 'rank' as URL parameters."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ranking')
def get_ranking():
    sorted_ranklist = dict(sorted(ranklist.items(), key=lambda item: item[1], reverse=True))
    enumerated_data = [(i, (institute, score)) for i, (institute, score) in enumerate(sorted_ranklist.items(), 1)]
    return render_template('ranking.html', data=enumerated_data)


@app.route('/predict' , methods=['POST'])
def predict_price():
    try:
        tlr = float(request.form.get('tlr'))
        rpc = float(request.form.get('rpc'))
        go = float(request.form.get('go'))
        oi = float(request.form.get('oi'))
        perception = float(request.form.get('perception'))

        global cur_data
        cur_data = str(request.form.get('institute'))
        
        new_data = pd.DataFrame({'tlr': [tlr], 'rpc': [rpc], 'go': [go], 'oi': [oi], 'perception': [perception]})
        score = model.predict(new_data)
        global cur_score
        cur_score = score

        return str(score[0])  # Assuming 'score' is a NumPy array, return the first element

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug = True)