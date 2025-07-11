# phospho-mcp-server
phospho's official MCP Server

This repository implements a **Model Context Protocol (MCP)** server for **Phosphobot**, enabling natural language interaction and control over a physical robot. It exposes tools to execute actions (e.g. pick up an object) and stream images from the robot's camera.

Built using [mcp](https://github.com/modelcontextprotocol/mcp) and tailored for Claude, ChatGPT, and other LLMs.

## Features

- 🔁 **Replay tool**: triggers a robot action from a dataset (e.g. pick up banana)
- 📷 **Camera stream**: retrieves the current webcam frame
- ⚙️ **Phosphobot wrapper**: manages local API processes and communication

---

## Tools

### `pickup_object`

> Launches a replay episode to simulate object manipulation.

```python
@mcp.tool()
def pickup_object(name: Literal["banana", "black circle", "green cross"]) -> str
````

* Launches a pre-recorded episode based on the object name.
* Currently supports:

  * `"banana"`
  * `"black circle"`
  * `"green cross"`

### `get_camera_frame`

> Captures a JPEG image from Phosphobot's camera.

```python
@mcp.tool()
def get_camera_frame() -> Image
```

* Uses the local Phosphobot API (`/frames`)
* Returns a base64-encoded JPEG image

---

## 🧱 Architecture

```bash
phospho-mcp-server/
│
├── server.py              # MCP server (FastMCP) with tools
├── tools/
│   ├── phosphobot.py      # Wrapper for phosphobot process and API
│   └── replay_api.py      # Tool to launch a replay
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

The `PhosphoBot` class is used to manage the `phosphobot` process lifecycle, and send GET/POST requests to its local API.

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
uv pip install -r requirements.txt
```

or (with MCP)

```bash
uv run --with mcp[cli] --with requests --with opencv-python --with pillow --with psutil
```

### 2. Start the MCP server

```bash
uv run --with mcp[cli] mcp run server.py
```

This will:

* Boot the MCP server under the name `"phosphobot-demo"`
* Register all tools with Claude or ChatGPT (if connected)

---

## 📡 How it works

The server communicates with a local instance of [phosphobot](https://robots.phospho.ai/) through its REST API (default `http://localhost:80`).

* `/frames` → image feed
* `/recording/play` → trigger replay from dataset

All calls are wrapped via `tools/phosphobot.py`.

---

## 🧪 Testing

### Replay from Claude / ChatGPT

Ask:

> “Pick up the banana”

Claude will call:

```json
{
  "tool": "pickup_object",
  "args": { "name": "banana" }
}
```

### Camera from Claude / ChatGPT

Ask:

> “What’s on my desk?”

Claude will call:

```json
{
  "tool": "get_camera_frame"
}
```

---

## 🧼 Cleanup

To manually stop `phosphobot`:

```bash
python -c "from tools.phosphobot import PhosphoBot; PhosphoBot().stop()"
```

---

## 📎 Notes

* If you're not using `uv`, just install dependencies manually.
* Make sure your webcam is not in use by another app.
* Phosphobot must be running for the tools to succeed.

---

## 📚 References

* [Model Context Protocol](https://modelcontextprotocol.io)
* [phosphobot](https://robots.phospho.ai/)
* [MCP Server Everything (reference)](https://github.com/modelcontextprotocol/server-everything)

```

---

Souhaites-tu aussi le `requirements.txt` ou un `Dockerfile` à inclure ?
```
