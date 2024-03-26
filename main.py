from fastapi import FastAPI

from database import create_tables

from router import config_router

import uvicorn

create_tables()
print("База готова к работе")

app = FastAPI()

app.title = "CONFIG KEEPER"

# добавление роутеров
app.include_router(config_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
