import argparse
import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server.
# stateless_http/json_response improve streamable-http behavior for remote clients.
mcp = FastMCP("weather", stateless_http=True, json_response=True)

# Constants
NWS_API_BASE = "https://api.weather.gov"
DEFAULT_USER_AGENT = "weather-app/1.0"


def get_user_agent() -> str:
    return os.getenv("WEATHER_USER_AGENT", DEFAULT_USER_AGENT)


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": get_user_agent(), "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    state_code = state.strip().upper()
    if len(state_code) != 2:
        return "State must be a two-letter US state code (example: CA, NY)."

    url = f"{NWS_API_BASE}/alerts/active/area/{state_code}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Weather MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default=os.getenv("MCP_TRANSPORT", "streamable-http"),
        help="Transport to run (default: streamable-http)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "127.0.0.1"),
        help="Bind host for HTTP/SSE transports (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "7000")),
        help="Bind port for HTTP/SSE transports (default: 7000)",
    )
    parser.add_argument(
        "--streamable-http-path",
        default=os.getenv("MCP_STREAMABLE_HTTP_PATH", "/mcp"),
        help="Path for streamable HTTP endpoint (default: /mcp)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Apply transport-related network settings from CLI/env before launching.
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.settings.streamable_http_path = args.streamable_http_path

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()