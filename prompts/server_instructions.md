# Weather MCP Server

This server provides tools for retrieving weather data from the US National Weather Service (NWS) API. It runs over streamable HTTP and requires Auth0 OAuth authentication.

## Authentication

The server uses Auth0 for token verification. Clients must provide a valid JWT with the `offline_access` scope. Tokens are verified against the configured Auth0 domain and audience using RS256 signing keys fetched from JWKS.

**Required environment variables:**
- `AUTH0_DOMAIN` - Auth0 tenant domain
- `AUTH0_AUDIENCE` - Expected audience claim for token verification
- `RESOURCE_SERVER_URL` - Resource server URL for OAuth settings

## Available Tools

### get_alerts
Retrieves active weather alerts for a US state.

**Parameters:**
- `state` (string): Two-letter US state code (e.g. CA, NY)

**Returns:** Formatted list of active alerts including event type, affected area, severity, description, and instructions. Returns a message if no alerts are found.

**Usage:** Call this tool to check for active weather warnings, watches, or advisories in a given state.

### get_forecast
Retrieves the weather forecast for a specific geographic location.

**Parameters:**
- `latitude` (float): Latitude of the location
- `longitude` (float): Longitude of the location

**Returns:** Forecast for the next few days depending on user input, with a maximum of 5 periods including temperature, wind speed/direction, and detailed forecast text.

**Usage:** Call this tool to get a multi-period weather forecast for any location within the US by providing its coordinates.