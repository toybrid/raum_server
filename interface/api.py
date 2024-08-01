from ninja import NinjaAPI
from ams.api import router as ams_router
from core.api import router as core_router
from account.api import router as auth_router


app = NinjaAPI(title="Raum")
app.add_router("", auth_router)
app.add_router("", ams_router)
app.add_router("", core_router)