from fastapi import APIRouter, Response
from typing import Annotated
from fastapi import Depends
from func_config import save_configuration, get_last_configuration
from schemas import Authdata


config_router = APIRouter(
    prefix="/config",
    tags=["Работа с конфигурациями"],
)


# def config_save(auth: Annotated[Authdata, Depends()], ):
@config_router.post("/save")
def config_save(auth: Authdata):
    rezult = Response(content=save_configuration(auth), media_type="text/plain")
    return rezult


@config_router.get("/get_last")
def config_get_last(device_ip: str):
    last_config = Response(content=get_last_configuration(device_ip), media_type="text/plain")
    return last_config
