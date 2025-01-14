"""
function: api接口
"""
from ninja import NinjaAPI
from apis.api import router as apis_router

api = NinjaAPI()

api.add_router("/", apis_router)
