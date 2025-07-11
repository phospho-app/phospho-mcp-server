from .phosphobot import PhosphoClient # type: ignore

def launch_replay(episode_id: int, phospho: PhosphoClient):
    phospho.post("/recording/play", json={
        "dataset_name": "mcp-demo",
        "episode_id": episode_id,
    })
