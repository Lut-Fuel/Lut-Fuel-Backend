import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional
from core.keys.keys import DATABASE_URL


# model = tf.keras.models.load_model('model.h5')
# scaler = joblib.load('scaler.joblib')

# app = FastAPI()

# class Car(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     maker: str
#     model: str
#     number_of_cylinders: int
#     engine_type: int
#     engine_horse_power: float
#     engine_horse_power_rpm: int
#     transmission: int
#     fuel_tank_capacity: int
#     acceleration_0_to_100_km: float
#     max_speed_km_per_hour: int
#     fuel_grade: int
#     year: int
#     type_of_car: int
#     car_name: str

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

# class UserInput(BaseModel):
#     Number_of_Cylinders: int
#     Engine_Type: int
#     Engine_Horse_Power: float
#     Engine_Horse_Power_RPM: int
#     Transmission: int
#     Fuel_Tank_Capacity: int
#     Acceleration_0_to_100_Km: float
#     Fuel_Grade: int




# if __name__ == '__main__':
#      uvicorn.run(app, host='127.0.0.1', port=8000)
# # # if __name__ == '__main__':
# # #     uvicorn.run(app, host='127.0.0.1', port=8000)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)
