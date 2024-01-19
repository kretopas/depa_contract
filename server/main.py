import uvicorn
from decouple import config

PORT = config("APP_PORT", default=3000, cast=int)
DEBUG = config("APP_DEBUG", default=False, cast=bool)

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=PORT, reload=DEBUG) 