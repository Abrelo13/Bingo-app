from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# ድረ-ገጹ እና ፓይዘኑ በነጻነት እንዲነጋገሩ መፍቀድ (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# የተጠቃሚዎችን የብር መጠን ለመያዝ (ጊዜያዊ ዳታቤዝ)
users_db = {}

@app.get("/")
def home():
    return {"status": "Bingo Backend is running successfully!"}

@app.get("/get-balance/{user_id}")
def get_balance(user_id: str):
    """የተጫዋቹን የኪስ ቦርሳ የብር መጠን ይልካል"""
    if user_id not in users_db:
        users_db[user_id] = {"balance": 100} # አዲስ ተጫዋች ከሆነ 100 ETB ስጦታ
    return {"balance": users_db[user_id]["balance"]}

@app.post("/start-game/{user_id}")
def start_game(user_id: str):
    """ጨዋታው ሲጀመር የዕድል ቁጥር ያወጣል"""
    if user_id not in users_db:
        users_db[user_id] = {"balance": 100}
        
    # ለአንድ ጨዋታ 20 ብር ይቀንሳል
    if users_db[user_id]["balance"] < 20:
        return {"error": "የበቂ ብር የለዎትም! እባክዎ አካውንትዎን ይሙሉ::"}
        
    users_db[user_id]["balance"] -= 20
    winning_number = random.randint(1, 25) # ከ 1 እስከ 25 የዕድል ቁጥር ማውጣት
    
    return {
        "balance": users_db[user_id]["balance"],
        "winning_number": winning_number,
        "message": f"የዕድል ቁጥር {winning_number} ወጥቷል!"
    }
