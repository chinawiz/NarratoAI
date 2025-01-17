import os
import uvicorn
from loguru import logger
from pyngrok import ngrok
from app.config import config

# Ensure pyngrok is installed
try:
    import pyngrok
except ImportError:
    os.system("pip install pyngrok")

if __name__ == "__main__":
    # Set up ngrok
    public_url = ngrok.connect(config.listen_port)
    logger.info(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{config.listen_port}\"")

    logger.info(
        "start server, docs: " + public_url + "/docs"
    )
    os.environ["HTTP_PROXY"] = config.proxy.get("http")
    os.environ["HTTPS_PROXY"] = config.proxy.get("https")
    uvicorn.run(
        app="app.asgi:app",
        host=config.listen_host,
        port=config.listen_port,
        reload=config.reload_debug,
        log_level="warning",
    )
