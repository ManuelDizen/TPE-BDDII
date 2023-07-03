from os import getenv

import uvicorn
import webbrowser
from dotenv import load_dotenv
from fastapi import FastAPI
from routes import galicia_user_router, pix_user_router, santander_user_router

from config import mongo, postgres

load_dotenv()

app = FastAPI()
app.include_router(galicia_user_router.router)
app.include_router(santander_user_router.router)
app.include_router(pix_user_router.router)
#
# Incluir los routers
#

@app.on_event("startup")
def start_application():
    mongo.start_connection()
    postgres.start_connection()

@app.on_event("shutdown")
def close_connection():
    mongo.close_connection()
    postgres.close_connection()

if __name__ == "__main__":
    port = getenv("API_PORT", 8000)
    webbrowser.open_new_tab("https://manueldizen-opulent-capybara-9w5q5w96prw2p447-8000.preview.app.github.dev/docs")
    if not port or not isinstance(port, int):
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)