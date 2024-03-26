# Config_keeper_v1


# запустить web сервер
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# обновить файл requirements.txt
pip freeze > requirements.txt