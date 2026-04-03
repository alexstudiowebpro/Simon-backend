import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyairtable import Api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autorise ton site Netlify à envoyer des données ici
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Récupération des clés secrètes (on les règlera sur Render)
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = "Commandes"

api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)

class OrderData(BaseModel):
    client: str
    whatsapp: str
    items: str
    total: int
    location: str

@app.get("/")
def home():
    return {"status": "Le serveur de Simon est en ligne !"}

@app.post("/commander")
async def receive_order(order: OrderData):
    try:
        table.create({
            "NOM_CLIENT": order.client,
            "WHATSAPP": order.whatsapp,
            "COMMANDE": order.items,
            "TOTAL": order.total,
            "LOCALISATION": order.location,
            "STATUT": "En attente"
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
