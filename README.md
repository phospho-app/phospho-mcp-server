# phospho-mcp-server
[phospho](https://docs.phospho.ai/)'s official MCP Server

This repository implements a **Model Context Protocol (MCP)** server for **phosphobot**, enabling natural language interaction and control over a physical robot. It exposes tools to execute actions (e.g. pick up an object) and stream images from cameras.

Built using [mcp](https://github.com/modelcontextprotocol/python-sdk) and tailored for Claude. 


https://github.com/user-attachments/assets/2d91f716-c581-4c36-94ab-cc5a94001468


## Features

- **Camera stream**: retrieves the current webcam frame
- **Replay tool**: triggers a robot action from a dataset (e.g. pick up banana)
- **phosphobot wrapper**: manages local API processes and communication


## Getting Started

### 1. Install and run phosphobot 

[phosphobot](https://docs.phospho.ai) is an [open source](https://github.com/phospho-app/phosphobot) software that lets you control robots, record data, train and use VLA (vision language action models).

Run this to install phosphobot:
```bash 
#macOS
curl -fsSL https://raw.githubusercontent.com/phospho-app/phosphobot/main/install.sh | bash

#Linux
curl -fsSL https://raw.githubusercontent.com/phospho-app/phosphobot/main/install.sh | sudo bash

#Windows
powershell -ExecutionPolicy ByPass -Command "irm https://raw.githubusercontent.com/phospho-app/phosphobot/main/install.ps1 | iex"
```

Run the phosphobot server:
```bash
phosphobot run
```

### 2. Install the MCP server in Claude Desktop

Make sure [Claude desktop](https://support.anthropic.com/en/articles/10065433-installing-claude-for-desktop) is installed. 

Install phospho-mcp-server this way using [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh # Install uv on MacOs or Linux
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # On Windows

# Clone repo
git clone https://github.com/phospho-app/phospho-mcp-server.git

# Install the server
cd phospho-mcp-server/phospho-mcp-server
uv run mcp install server.py
```

This will:

* Boot the MCP server under the name `phospho`
* Register all tools with 

Now, open Claude desktop. You should see the phospho MCP server listed along the tools.  


## How it works

The server speaks to a local instance of [phosphobot](https://robots.phospho.ai/) through its REST API (default `http://localhost:80`).

* `/frames` → image feed
* `/recording/play` → trigger replay from dataset

All calls are wrapped via `tools/phosphobot.py`. If you run phosphobot on a different port, you need to modify the base URL.

---

## Development and testing

To test your server with the MCP inspector, run:
```bash 
uv run mcp dev server.py
```

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

The `PhosphoClient` class is used to manage the `phosphobot` process lifecycle, and send GET/POST requests to its local API.


---

## References

* [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
* [phosphobot](https://docs.phospho.ai/installation)
