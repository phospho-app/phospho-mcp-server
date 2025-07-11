import tempfile
from typing import Literal, cast
import cv2
from mcp.server.fastmcp import FastMCP, Image
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
import requests

from tools.replay_api import launch_replay
from tools.phosphobot import PhosphoBot
from PIL import Image as PILImage
import base64
from io import BytesIO
import platform


# Object-to-episode mapping
OBJECT_TO_EPISODE = {
    "banana": 0,
    "black circle": 1,
    "green cross": 2,
}

@dataclass
class AppContext:
    phospho: PhosphoBot

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    print("Starting Phosphobot...")
    # start_phosphobot()
    # wait_for_phosphobot()  # Important pour ne pas exécuter les tools trop tôt
    phospho = PhosphoBot()
    try:
        yield AppContext(phospho=phospho)
    finally:
        print("Stopping Phosphobot...")
        # phospho.stop()

# Create server with lifespan
mcp = FastMCP("phosphobot-demo", lifespan=app_lifespan, dependencies=["requests", "opencv-python-headless", "pillow", "psutil"])


@mcp.tool()
def pickup_object(name: Literal["banana", "black circle", "green cross"]) -> str:
    ctx = mcp.get_context()
    app_ctx = cast(AppContext, ctx.request_context.lifespan_context)
    episode_id = OBJECT_TO_EPISODE.get(name)
    if episode_id is None:
        return f"Unknown object: {name}"
    launch_replay(episode_id=episode_id, phospho=app_ctx.phospho)
    return f"Launched replay for {name}."

@mcp.tool()
def get_camera_frame() -> Image:
    """
    Récupère une image depuis le flux webcam du robot (via API phosphobot).
    """
    result = PhosphoBot().get("/frames")
    
    if not isinstance(result, dict):
        raise RuntimeError("Invalid response from phosphobot")

    # Choisir la première caméra disponible (ex: "0", "realsense", etc.)
    image_b64 = result.get("0") or next(iter(result.values()), None)

    if not image_b64:
        raise RuntimeError("No camera frame returned")

    try:
        return Image(
            data=base64.b64decode(image_b64),
            format="jpeg"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to decode image: {e}")



