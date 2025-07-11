from .phosphobot import PhosphoBot

def launch_replay(episode_id: int, phospho: PhosphoBot):
    phospho.post("/recording/play", json={
        "dataset_name": "mcp-demo",
        "episode_id": episode_id,
    })
