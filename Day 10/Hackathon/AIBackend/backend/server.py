import logging
import uvicorn

# from backend.config.main import PORT

logging.basicConfig(level=logging.INFO)


def start_server():
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=5002,
        reload=True,
    )


if __name__ == "__main__":
    start_server()
