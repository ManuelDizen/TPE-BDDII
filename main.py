from os import getenv

import uvicorn
import webbrowser
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routes import galicia_user_router, frances_user_router, pix_user_router, santander_user_router

from config import mongo, postgres, couch, save_updated_cbus

load_dotenv()

app = FastAPI(title='TPE - BDDII - "Pixies"',
              description='Esta página documenta todos los endpoints desarrollados con FastAPI para interactuar con la aplicación')
app.include_router(galicia_user_router.router)
app.include_router(santander_user_router.router)
app.include_router(frances_user_router.router)
app.include_router(pix_user_router.router)

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trabajo Práctico Especial - Base de Datos II - 1Q2023<br>Equipo "Pixies"</title>
        <style>
            body {
                background-color: #f2f2f2;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 800px;
                height: 80vh;
                margin: 5vh 5vw;
                padding: 30px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                background-color: #ffffff;
            }
            .left-column {
                flex: 0 0 50%;
            }
            .right-column {
                flex: 0 0 50%;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            h1 {
                color: #333333;
                font-size: 28px;
                margin-bottom: 20px;
            }
            p {
                color: #666666;
                font-size: 16px;
                margin-bottom: 30px;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                text-decoration: none;
                background-color: #4CAF50;
                color: #ffffff;
                border-radius: 4px;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #45a049;
            }
            .image-container {
                max-width: 100%;
                height: auto;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="left-column">
                <h1>Trabajo Práctico Especial - Base de Datos II - 1Q2023<br>Equipo "Pixies"</h1>
                <p>Bienvenidos al trabajo práctico del equipo "Pixies" para el final de la materia.<br>Clickeando el botón de abajo, se podrá acceder a la documentación de la API, ofrecida por Swagger.</p>
                <a class="button" href="/docs">Ver API</a>
            </div>
            <div class="right-column">
                <img class="image-container" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fvignette.wikia.nocookie.net%2Ffarilyoddparents%2Fimages%2F7%2F7c%2FTitlecard-Pixies_Inc.jpg%2Frevision%2Flatest%3Fcb%3D20120722210240&f=1&nofb=1&ipt=e203a300b788056c44be1d564d4ce91fb08abb12a13423b0016f5e34bdffea1d&ipo=images" alt="Image Description">
            </div>
        </div>
    </body>
    </html>
    """

#
# Incluir los routers
#

@app.on_event("startup")
def start_application():
    mongo.start_connection()
    postgres.start_connection()
    couch.start_connection()

@app.on_event("shutdown")
def close_connection():
    mongo.close_connection()
    postgres.close_connection()
#    couch.close_connection()
    save_updated_cbus()


if __name__ == "__main__":
    port = getenv("API_PORT", 8000)
    if not port or not isinstance(port, int):
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port, root_path="/docs")