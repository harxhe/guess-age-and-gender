#this is a simple server made that uses ageify and genderize api to predict the age and gender of a person based on their name 

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
from mangum import Mangum 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(request: Request, name: str = Form(...)):
    async with httpx.AsyncClient() as client:     #sending async request to the api without blocking the next request
        age_response = await client.get(f"https://api.agify.io/?name={name}")
        gender_response = await client.get(f"https://api.genderize.io/?name={name}")

    print("Age API Response:", age_response.json())
    print("Gender API Response:", gender_response.json())

    age_data = age_response.json()
    gender_data = gender_response.json()
    
    #json parsing to get the age and gender
    age = age_data.get("age", "not available") 
    gender = gender_data.get("gender", "not available")

    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "person_name": name, "person_age": age, "person_gender": gender}
    )

handler = Mangum(app)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
