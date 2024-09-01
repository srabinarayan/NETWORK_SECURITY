import os
import sys
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.pipelines.training_pipeline import TrainingPipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse


from networksecurity.utils.modelling_utils.estimator import ModelResolver
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR

from networksecurity.utils.common_utils.utils import load_object
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

os.environ["AWS_ACCESS_KEY_ID"]=AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"]=AWS_SECRET_ACCESS_KEY


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run()
        return Response("Training successful !!")
    except Exception as e:
            raise NetworkSecurityException(e,sys)

@app.get("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        model = ModelResolver(model_dir=SAVED_MODEL_DIR)
        latest_model_path = model.get_best_model_path()
        latest_model = load_object(file_path=latest_model_path)
        
        y_pred = latest_model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        table_html = df.to_html(classes='table table-striped')
        
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
            raise NetworkSecurityException(e,sys)
def set_env_variable(env_file_path):
    pass

# def main():
#     try:
#         set_env_variable(env_file_path)
#         training_pipeline = TrainPipeline()
#         training_pipeline.run() 
#     except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
if __name__=="__main__":
    # main()
    # set_env_variable(env_file_path)
    app_run(app, host="localhost", port=8000)                        
