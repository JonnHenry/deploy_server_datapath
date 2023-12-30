from fastapi import APIRouter , HTTPException, status
from models import Prediction_Input, Prediction_Output,Message_Prediction,Message_Error
import pandas as pd
import numpy as np
from joblib import load
from typing import Union

MODEL_PATH = 'rf_classifier_model.joblib'
SCALER_PATH = 'scaler_model.joblib'

# Load model
model = load(MODEL_PATH)
scalar = load(SCALER_PATH)

def standarize(data):
    ever_married_mapping = {'no': 0, 'yes': 1, np.nan : 2}
    work_type_mapping = {'never_worked': 0, 'govt_job': 1, 'self_employed': 2, 'children' : 3, 'private' : 4, np.nan : 5}
    data_standarize = {}
    data_standarize["age"] = data.age
    data_standarize["hypertension"] = data.hypertension
    data_standarize["heart_disease"] = data.heart_disease
    data_standarize["ever_married"] = ever_married_mapping[data.ever_married]
    data_standarize["work_type"] = work_type_mapping[data.work_type]
    return data_standarize

router = APIRouter()

preds = []

@router.get('/stroke', response_model=list[Prediction_Output])
def get_stroke():
    return preds

@router.post('/stroke',status_code=status.HTTP_201_CREATED,response_model=Prediction_Output)
def create_stroke(pred_input: Prediction_Input):
    data_standarize = standarize(pred_input)
    scalar_input = scalar.transform(pd.DataFrame([data_standarize]))
    prediction = model.predict(scalar_input)
    predict_dict= {"id": len(preds)+1,
                    "stroke_input":pred_input.dict(),
                    "pred": prediction[0] }
    preds.append(predict_dict)
    return predict_dict


@router.put('/stroke/{pred_id}',response_model=Union[Prediction_Output,Message_Error])
def put_stroke(pred_id:int,pred_input: Prediction_Input):
    for index, item in enumerate(preds):
        if item["id"] == pred_id:
            data_standarize = standarize(pred_input)
            scalar_input = scalar.transform(pd.DataFrame([data_standarize]))
            prediction = model.predict(scalar_input)
            item["stroke_input"] = pred_input.dict()
            item["pred"] = prediction[0]
            preds[index] = item
            return {"id": item["id"],
                    "stroke_input":item["stroke_input"],
                    "pred": item["pred"] }
    else:
        return HTTPException(status_code=404,detail="Prediction not found")



@router.delete('/stroke/{pred_id}',response_model=Union[Message_Prediction,Message_Error])
def del_stroke(pred_id:int):
    for index, item in enumerate(preds):
        if item["id"] == pred_id:
            preds.pop(index)
            print(index)
            return {"message": "Prediction deleted"}
    else:
        return HTTPException(status_code=404,detail="Prediction not found")