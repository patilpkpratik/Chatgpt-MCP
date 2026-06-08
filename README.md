# Weather MCP Server

MCP server that exposes weather tools backed by the US National Weather Service API.

## Tools

- `get_alerts(state: str)`
- `get_forecast(latitude: float, longitude: float)`

## Requirements

- Python 3.10+
- `uv` (recommended) or `pip`

Note: this project will not install on Python 3.9.

## Install

### Option A: uv (recommended)

```bash
uv sync
```

### Option B: pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuration

Copy and customize the environment template:

```bash
cp .env.example .env
```

Key variables:

- `MCP_TRANSPORT`: `stdio`, `streamable-http`, or `sse`
- `MCP_HOST`: host bind for HTTP/SSE modes
- `MCP_PORT`: port bind for HTTP/SSE modes
- `MCP_STREAMABLE_HTTP_PATH`: streamable HTTP route (default `/mcp`)
- `MCP_SSE_PATH`: SSE route (default `/sse`)
- `WEATHER_USER_AGENT`: optional NWS user-agent override

## Run Modes

### 1) Local stdio mode (for local MCP clients)

```bash
uv run weather.py --transport stdio
```

### 2) Streamable HTTP mode (for ChatGPT Web connectivity)

```bash
uv run weather.py --transport streamable-http
```

By default, the streamable HTTP endpoint is available at:

- `http://localhost:8000/mcp`

You can also override host/port/path directly:

```bash
uv run weather.py --transport streamable-http --host 0.0.0.0 --port 8080 --streamable-http-path /mcp
```

## Connect to ChatGPT Web

ChatGPT Web cannot directly spawn local stdio processes. You must provide a reachable MCP URL.

1. Start the server in streamable HTTP mode.
2. Expose localhost via a secure tunnel (for example, Cloudflare Tunnel or ngrok).
3. Copy the HTTPS URL for your `/mcp` endpoint.
4. In ChatGPT, open Settings -> Apps.
5. Add a custom app using your MCP server URL.
6. Confirm tools are discoverable and run test prompts.

Example tunnel commands:

```bash
# ngrok
ngrok http 8000

# cloudflared
cloudflared tunnel --url http://localhost:8000
```

If your tunnel URL is `https://demo.example.ngrok-free.app`, use:

- `https://demo.example.ngrok-free.app/mcp`

Example test prompts:

- "Use weather tools to get active alerts for CA"
- "Use weather tools to get the forecast for 40.7128, -74.0060"

## Troubleshooting

- If dependency install fails, ensure `uv` is up to date.
- If `uv sync` fails with proxy authorization while downloading Python, configure your proxy credentials or use a preinstalled local Python 3.10+.
- If `pip install -e .` fails with "requires a different Python", switch to Python 3.10+ first.
- If tool calls fail, check that `api.weather.gov` is reachable.
- If ChatGPT cannot connect, verify your public HTTPS tunnel URL resolves to `/mcp`.
- If ChatGPT cannot connect, verify host/port/path values match your tunnel target.
- If there are no alerts for a state, the tool may correctly return no active alerts.

## Security Notes

- This server is read-only with respect to weather data.
- Do not expose development servers publicly without access controls.
- Review app permissions in ChatGPT before enabling broad usage.
