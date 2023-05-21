import uvicorn
from app import app
from core.db import database
import routes
from dotenv import load_dotenv

load_dotenv()

app.include_router(routes.router)


app.state.database = database


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(8000))
