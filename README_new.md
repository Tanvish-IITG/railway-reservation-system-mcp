# Railway Reservation System - MCP Server

A Model Context Protocol (MCP) server for checking railway seat availability. This server provides Claude with the ability to check train seat availability, berth types, and pricing information.

## Features

- **Seat Availability Checking**: Get real-time availability for different train classes
- **Berth Type Information**: Upper, middle, and lower berth availability and pricing
- **Comprehensive Details**: Train schedules, route information, and booking status
- **Alternative Options**: Suggested alternative trains when preferred options are unavailable

## Installation

### For MCP Server Usage with Claude

1. Install the MCP library:
```bash
pip install mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### For Standalone Usage

The server can also run independently without MCP for testing:
```bash
python mcp-server.py
```

## Configuration for Claude Desktop

Add this configuration to your Claude Desktop config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "railway-reservation-system": {
      "command": "python",
      "args": ["mcp-server.py"],
      "cwd": "t:\\code\\mcp\\railway-reservation-system"
    }
  }
}
```

## Available Tools

### check_seat_availability

Check seat availability for railway reservations.

**Parameters:**
- `train_name` (string): Name of the train (e.g., "Rajdhani Express")
- `travel_date` (string): Date of travel in YYYY-MM-DD format
- `start_station` (string): Starting station name or code
- `end_station` (string): Destination station name or code  
- `travel_class` (string): Class of travel (AC1, AC2, AC3, Sleeper, CC, EC, 2S)

**Returns:**
Comprehensive JSON with:
- Train details and schedule
- Seat availability by berth type (upper, middle, lower)
- Pricing information
- Booking status and policies
- Alternative train options

## Example Usage with Claude

Once configured, you can ask Claude:

- "Check seat availability for Rajdhani Express from Delhi to Mumbai on July 15th in AC2 class"
- "What are the available berths in Shatabdi Express for tomorrow?"
- "Show me pricing for different berth types in AC3 class"

## Sample Response

```json
{
  "train_details": {
    "train_name": "Rajdhani Express",
    "train_number": "12001",
    "travel_date": "2025-07-15",
    "route": {
      "start_station": "New Delhi (NDLS)",
      "end_station": "Mumbai Central (BCT)",
      "departure_time": "08:30",
      "arrival_time": "14:45",
      "duration": "6h 15m"
    }
  },
  "class_availability": {
    "AC2": {
      "total_seats": 72,
      "available_seats": 18,
      "berth_availability": {
        "upper": {
          "total": 24,
          "available": 6,
          "price": 1250.0
        },
        "middle": {
          "total": 24,
          "available": 4,
          "price": 1275.0
        },
        "lower": {
          "total": 24,
          "available": 8,
          "price": 1300.0
        }
      }
    }
  }
}
```

## Development

To extend this server:

1. Modify the `check_seat_availability` function to connect to real railway APIs
2. Add new tools for booking, cancellation, or PNR status
3. Implement authentication for accessing real booking systems
4. Add caching for better performance

## Files

- `mcp-server.py`: Main MCP server implementation
- `requirements.txt`: Python dependencies
- `claude_desktop_config.json`: Sample Claude configuration
- `README.md`: This documentation

## License

This project is provided as-is for educational and development purposes.
