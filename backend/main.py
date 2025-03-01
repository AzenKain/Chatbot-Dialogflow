from fastapi import FastAPI, Request
import logging
from fastapi.middleware.cors import CORSMiddleware
import joblib

loaded_model = joblib.load('decision_tree_model.pkl')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mapping_data = {
    "luong mua it": 0,
    "luong mua nhieu": 40,
    "luong mua binh thuong": 10,
    "gio nhe": 2,
    "gio manh": 5,
    "gio binh thuong": 3.2,
    "nhiet do thap": 7,
    "nhiet do cap": 30,
    "nhiet do binh thuong": 12,
}

weather_mapping = {
  0: "trời có thể có mưa phùn",
  1: "trời có thể có sương mù",
  2: "trời có thể mưa",
  3: "trời có thể có tuyết rơi",
  4: "trời có thể có nắng"
}


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/dialogflow")
async def handler_dialogflow(request: Request):
    try:
        req_json = await request.json()
        parameters = req_json.get("queryResult", {}).get("parameters", {})
        filtered_params = {k: v for k, v in parameters.items() if v != ''}
        tempera = [v for v in [filtered_params.get("nhiet-do"), filtered_params.get("temperature")] if v]
        precipitation = [v for v in [filtered_params.get("do-am"), filtered_params.get("unit-length")] if v]
        wind = [v for v in [filtered_params.get("gio"), filtered_params.get("unit-speed")] if v]
        month = [v for v in [filtered_params.get("date-time")]]
        process = [[]]
        if len(tempera) == 0 or len(precipitation) == 0 or len(wind) == 0:
            return {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": ["Thiếu hoặc sai dữ liệu vui lòng nhập lại!"]
                        }
                    }
                ]
            }

        if isinstance(precipitation[0], dict):
            amount = precipitation[0].get("amount")
            unit = precipitation[0].get("unit")
            if unit == "cm":
                amount *= 10
            elif unit == "m":
                amount *= 1000
            elif unit == "inch":
                amount *= 25.4
            process[0].append(amount)
        else:
            process[0].append(mapping_data.get(precipitation[0]))

        if isinstance(wind[0], dict):
            amount = wind[0].get("amount")
            unit = wind[0].get("unit")
            if unit == "km h":
                amount = amount / 3.6
            process[0].append(amount)
        else:
            process[0].append(mapping_data.get(wind[0]))

        if month:
            end_date = month[0].get("endDate")
            if end_date:
                month_num = end_date.split('-')[1]
                process[0].append(int(month_num))

        if isinstance(tempera[0], dict):
            amount = tempera[0].get("amount")
            unit = tempera[0].get("unit")
            if unit == "K":
                amount = amount - 273.15
            process[0].append(amount)
        else:
            process[0].append(mapping_data.get(tempera[0]))

        prediction = loaded_model.predict(process)

        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [f"Theo tôi dự đoán thì {weather_mapping[prediction[0]]}.\nBạn muốn dự đoán tiếp không?"]
                    }
                }
            ]
        }

    except Exception as err:
        print(f'could not process REQUEST: {err}')
        return {"status": "ERR"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
