from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Code Academy")

# Images folder
app.mount("/images", StaticFiles(directory="images"), name="images")


# Home page
@app.get("/")
def home():
    return FileResponse("index.html")


# Course page
@app.get("/course")
def course():
    return FileResponse("course.html")


# Advertisement API
@app.get("/api/ad")
def get_ad():
    return {
        "company": "Code Academy",
        "title": "Learn Python",
        "description": "Master Python from beginner to advanced.",
        "discount": "50% OFF",
        "offer": "Special Offer: Get our Python Course at 50% discount!",
        "button": "Claim Offer",
        "image": "/images/ad.jpg",
        "link": "/course"
    }