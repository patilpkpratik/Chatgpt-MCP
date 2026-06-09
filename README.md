
# 🌤️ MCP Weather App

This project is a simple **MCP (Model Context Protocol)** server tool that provides real-time weather information based on natural language queries like:

> "What's the weather in Bangalore?"

It uses:
- 🧠 `mcp` to expose the weather tool
- 📍 `geopy` (Nominatim) to convert location names to coordinates
- 🌐 Open-Meteo API to fetch live weather data

---

## 🚀 How It Works

### Tool: `open_weather_app(query)`
The main MCP tool that:
1. Extracts the location from the user query
2. Geocodes the location name to latitude/longitude
3. Calls Open-Meteo API to get current weather
4. Returns a weather summary

### 📦 Key Components

- `extract_location(query: str)`  
  Parses user queries like `"weather in New York"` or `"Mumbai weather"` and extracts just the location.

- `get_lat_lon(location_name)`  
  Uses `geopy.geocoders.Nominatim` to convert location names into GPS coordinates.

- `get_weather(lat, lon)`  
  Fetches weather data from the Open-Meteo API and formats it using a custom description dictionary.

---

## Example Usage

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather App")

@mcp.tool()
def open_weather_app(query):
    ...
```

Query:
```
What's the weather in Bangalore?
```

Response:
```
Weather: {
  "temperature": "29 °C",
  "windspeed": "10 km/h",
  "weathercode": "Clear sky"
}
```

---

## 📥 Requirements

- `mcp`
- `geopy`
- `requests`

Install them using:
```bash
uv init .
```
```bash
uv add "mcp[cli]" geopy requests
```

---

## 📌 Notes

- The geolocation is done using OpenStreetMap via `Nominatim`
- The weather API used is [https://open-meteo.com](https://open-meteo.com)

- To add MCP server to claude desktop app:  
  ```bash
  uv run mcp install main.py 
  ```
- Restart the cluaude desktop app
---

