from sklearn.pipeline import make_pipeline
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle



def create_app():
    app = Flask(__name__)
    
    with open('./flask_app/model/model.p', 'rb') as file:
        model = pickle.load(file)
        encoder = pickle.load(file)
    


    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/car-info', methods=['GET', 'POST'])
    def survey():
        return render_template('car-info.html')

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/car-price', methods=['POST'])
    def modeling():
        Manufacturer = request.form['Manufacturer']
        Model = request.form['Model']
        Km = request.form['Km']
        Fuel = request.form['Fuel']
        Loc = request.form['Loc']
        Old_year = request.form['Old_year']
        Old_month = request.form['Old_month']


        car_info = pd.DataFrame(columns=['Manufacturer', 'Model', 'Km', 'Fuel', 'Loc', 'Old_year', 'Old_month'])
        car_info['Manufacturer'] = [Manufacturer]
        car_info['Model'] = [Model]
        car_info['Km'] = int(Km)
        car_info['Fuel'] = [Fuel]
        car_info['Loc'] = [Loc]
        car_info['Old_year'] = int(Old_year)
        car_info['Old_month'] = int(Old_month)
        cat_cols = car_info.columns[car_info.dtypes == object]

        car_info[cat_cols] = encoder.transform(car_info[cat_cols])
        
        pred = model.predict(car_info)[0]
        output = round(pred)
        return render_template('result.html', data=output)
    
    
    return app

if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)



