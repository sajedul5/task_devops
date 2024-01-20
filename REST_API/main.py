from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
import socket
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class WeatherInfo(BaseModel):
    temperature: str
    temp_unit: str

@app.get("/api/hello")
async def hello():
    hostname = socket.gethostname()
    current_datetime = datetime.now().strftime('%y%m%d%H%M')
    version = '1.0'

    weather_data = await get_weather_data()

    response_data = {
        "hostname": hostname,
        "datetime": current_datetime,
        "version": version,
        "weather": {"dhaka": weather_data}
    }

    return response_data

@app.get("/health")
async def health_check():
    return {"status": "OK"}

async def get_weather_data():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://api.openweathermap.org/data/2.5/weather?q=Dhaka&appid={os.getenv('OPENWEATHERMAP_API_KEY')}")
            response.raise_for_status()
            data = response.json()
            temperature = str(data['main']['temp'])
            temp_unit = 'C'  # Assuming temperature is in Celsius
            return {"temperature": temperature, "temp_unit": temp_unit}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
