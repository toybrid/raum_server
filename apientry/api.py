from ninja import NinjaAPI
from ams.api.v1.api import router as ams_router


app_v01 = NinjaAPI(title="Raum", version="0.1.0")

app_v01.add_router("", ams_router)