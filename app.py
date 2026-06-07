import os
import sys
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse
# from starlette.responses import RedirectResponse
import uvicorn

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity import logger
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from fastapi.templating import Jinja2Templates

# تنظیمات مربوط به دیتابیس SQLite (اگر نیاز به خواندن مستقیم داری)
# اما پایپ‌لاین آموزشی خودش از sqlite استفاده می‌کند، پس اینجا فقط API را تعریف می‌کنیم.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)
origins = ["*"]

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
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# بخش مربوط به Prediction در مرحله بعد اضافه خواهد شد

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # 1. خواندن فایل آپلود شده توسط کاربر
        df = pd.read_csv(file.file)
        # print(df)

        # 2. بارگذاری مدل و پیش‌پردازشگر از پوشه نهایی
        preprocessor = load_object("final_models/preprocessor.pkl")
        final_model = load_object("final_models/model.pkl")

        # 3. ساختن شیء مدل برای پیش‌بینی
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        # چاپ اولین ردیف برای تست در کنسول
        print(df.iloc[0])

        # 4. انجام پیش‌بینی روی کل داده‌های فایل
        y_pred = network_model.predict(df)
        print(y_pred)

        # 5. اضافه کردن ستون نتیجه به دیتافریم
        df['predicted_column'] = y_pred
        print(df['predicted_column'])

        # اختیاری: جایگزینی مقادیر (اگر در دیتاست شما -1 به معنای دیگری است)
        # df['predicted_column'].replace(-1, 0)

        # 6. تبدیل دیتافریم به کد HTML با استایل کلاس‌های بوت‌استرپ
        df.to_csv("prediction_output/prediction.csv")
        table_html = df.to_html(classes='table table-striped')
        # print(table_html)

        # 7. رندر کردن و فرستادن نتیجه به فایل table.html
        return templates.TemplateResponse(
                request=request,
                name="table.html",
                context={
                    "request": request,
                    "table": table_html
                }
)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
