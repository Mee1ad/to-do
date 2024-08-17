# Run command in windows

cd /d e:/to-do & E:/to-do/.venv/Scripts/activate & uvicorn main:app --reload --port 5000
cd /d e:/dev/to-do & E:/dev/to-do/.venv/Scripts/activate & uvicorn main:app --reload --port 5000

# db initialization

from db.init import *
create_tables()


