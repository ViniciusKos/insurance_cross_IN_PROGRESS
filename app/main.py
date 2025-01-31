import pickle
import pandas as pd
from flask import Flask, request, Response
from insurance import Insurance, data_cleaning, FeatureEngineering
# from sklearn.base import BaseEstimator, TransformerMixin
# from category_encoders.target_encoder import TargetEncoder

import __main__
__main__.data_cleaning = data_cleaning
__main__.FeatureEngineering = FeatureEngineering
__main__.Insurance = Insurance




# loading model
model = pickle.load( open(r'parameters/model.pkl', 'rb') )

# initialize API
app = Flask( __name__ )
@app.route( r'/predict', methods=['POST'] )
def insurance_predict():
    test_json = request.get_json()
   
    if test_json: # there is data
        if isinstance( test_json, dict ): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
            
        # Instantiate Insurance class
        pipeline = Insurance()
        
        #data cleaning
        df1 = pipeline.data_cleaning( test_raw )
        
        # feature engineering
        df2 = pipeline.feature_engineering( df1 )
        
        # data preparation
        df3 = pipeline.data_preparation( df2 )
        
        # prediction
        df_response = pipeline.get_prediction( model, test_raw, df3 )
        
        return df_response
        
        
    else:
        return Response( '{}', status=200, mimetype='application/json' )

if __name__ == '__main__':
    app.run( '' ,debug=True)