# phospho-mcp-server
[phospho](https://robots.phospho.ai/)'s official MCP Server

This repository implements a **Model Context Protocol (MCP)** server for **phosphobot**, enabling natural language interaction and control over a physical robot. It exposes tools to execute actions (e.g. pick up an object) and stream images from cameras.

Built using [mcp](https://github.com/modelcontextprotocol/python-sdk) and tailored for Claude. 

## Features

- **Camera stream**: retrieves the current webcam frame
- **Replay tool**: triggers a robot action from a dataset (e.g. pick up banana)
- **phosphobot wrapper**: manages local API processes and communication

---

## Tools

### `pickup_object`

> Launches a replay episode to simulate object manipulation.

```python
@mcp.tool()
def pickup_object(name: Literal["banana", "black circle", "green cross"]) -> str
````

* Launches a pre-recorded episode based on the object name.

### `get_camera_frame`

> Captures a JPEG image from phosphobot's camera.

```python
@mcp.tool()
def get_camera_frame() -> Image
```

* Uses the local phosphobot API (`/frames`)
* Returns a base64-encoded JPEG image

---

## Architecture

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

## Getting Started

### 1. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 2. Install and run phosphobot 

Installation:
```bash 
#macOS
curl -fsSL https://raw.githubusercontent.com/phospho-app/phosphobot/main/install.sh | bash

#Linux
curl -fsSL https://raw.githubusercontent.com/phospho-app/phosphobot/main/install.sh | sudo bash

#Windows
powershell -ExecutionPolicy ByPass -Command "irm https://raw.githubusercontent.com/phospho-app/phosphobot/main/install.ps1 | iex"
```
Then, run the phosphobot server:
```bash
phosphobot run
```

### 3. Install the MCP server in Claude Desktop and interact with it

```bash 
uv run mcp install server.py
```
This will:

* Boot the MCP server under the name `"phosphobot-demo"`
* Register all tools with Claude 

To test your server with the MCP inspector, run:
```bash 
uv run mcp dev server.py
```

## How it works

The server communicates with a local instance of [phosphobot](https://robots.phospho.ai/) through its REST API (default `http://localhost:80`).

* `/frames` → image feed
* `/recording/play` → trigger replay from dataset

All calls are wrapped via `tools/phosphobot.py`.

---

## Testing

### Camera from Claude 

Ask:

> “What’s on my desk?”

Claude will call:

```json
{
  "tool": "get_camera_frame"
}
```

### Replay from Claude 

Ask:

> “Pick up the banana”

Claude will call:

```json
{
  "tool": "pickup_object",
  "args": { "name": "banana" }
}
```

---

## Notes

* If you're not using `uv`, just install dependencies manually.
* phosphobot must be running for the tools to succeed.

---

## 📚 References

* [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
* [phosphobot](https://docs.phospho.ai/installation)
