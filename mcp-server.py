#!/usr/bin/env python3

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List

# Try to import MCP dependencies, fall back to standalone mode if not available
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
        LoggingLevel
    )
    import mcp.types as types
    MCP_AVAILABLE = True
except ImportError:
    print("MCP library not found. Running in standalone mode.")
    print("To use as MCP server, install with: pip install mcp")
    MCP_AVAILABLE = False

if MCP_AVAILABLE:
    # Create the server instance
    server = Server("railway-reservation-system")


    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        """
        List available tools.
        Each tool should have a name, description, and parameters.
        """
        return [
            Tool(
                name="check_seat_availability",
                description="Check seat availability for railway reservations. Returns availability for different berth types (upper, middle, lower) along with pricing and booking status.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "train_name": {
                            "type": "string",
                            "description": "Name of the train (e.g., 'Rajdhani Express', 'Shatabdi Express')"
                        },
                        "travel_date": {
                            "type": "string",
                            "description": "Date of travel in YYYY-MM-DD format"
                        },
                        "start_station": {
                            "type": "string", 
                            "description": "Starting station name or code (e.g., 'New Delhi', 'NDLS')"
                        },
                        "end_station": {
                            "type": "string",
                            "description": "Destination station name or code (e.g., 'Mumbai Central', 'BCT')"
                        },
                        "travel_class": {
                            "type": "string",
                            "description": "Class of travel (AC1, AC2, AC3, Sleeper, CC, EC, etc.)",
                            "enum": ["AC1", "AC2", "AC3", "Sleeper", "CC", "EC", "2S"]
                        }
                    },
                    "required": ["train_name", "travel_date", "start_station", "end_station", "travel_class"]
                }
            )
        ]


    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
        """
        Handle tool calls from the client.
        """
        if name == "check_seat_availability":
            result = await check_seat_availability(
                train_name=arguments["train_name"],
                travel_date=arguments["travel_date"], 
                start_station=arguments["start_station"],
                end_station=arguments["end_station"],
                travel_class=arguments["travel_class"]
            )
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )
            ]
        else:
            raise ValueError(f"Unknown tool: {name}")


async def check_seat_availability(
    train_name: str,
    travel_date: str,
    start_station: str,
    end_station: str,
    travel_class: str
) -> Dict[str, Any]:
    """
    Check seat availability for a given train and route.
    
    Args:
        train_name (str): Name of the train (e.g., "Rajdhani Express")
        travel_date (str): Date of travel in YYYY-MM-DD format
        start_station (str): Starting station code/name
        end_station (str): Destination station code/name
        travel_class (str): Class of travel (AC1, AC2, AC3, Sleeper, etc.)
    
    Returns:
        Dict[str, Any]: JSON response with availability details
    """
    
    # Sample availability data - in real implementation, this would query a database
    availability_data = {
        "train_details": {
            "train_name": train_name,
            "train_number": "12001",  # Sample train number
            "travel_date": travel_date,
            "route": {
                "start_station": start_station,
                "end_station": end_station,
                "departure_time": "08:30",
                "arrival_time": "14:45",
                "duration": "6h 15m"
            }
        },
        "class_availability": {
            travel_class: {
                "total_seats": 72,
                "available_seats": 18,
                "waiting_list": 5,
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
                },
                "status": "Available" if 18 > 0 else "Waiting List",
                "base_fare": 1200.0,
                "booking_status": "OPEN"
            }
        },
        "additional_info": {
            "tatkal_available": True,
            "premium_tatkal_available": False,
            "cancellation_charges": {
                "upto_4_hours": "25% of fare",
                "4_to_12_hours": "50% of fare",
                "after_12_hours": "No refund"
            },
            "booking_counter": "IRCTC Online",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "alternate_options": [
            {
                "train_name": "Shatabdi Express",
                "train_number": "12002",
                "departure_time": "10:15",
                "available_seats": 32,
                "class": travel_class
            },
            {
                "train_name": "Mail Express",
                "train_number": "12003", 
                "departure_time": "16:30",
                "available_seats": 45,
                "class": travel_class
            }
        ]
    }
    
    return availability_data


async def main():
    """
    Main function to run the MCP server or standalone demo.
    """
    if MCP_AVAILABLE:
        # Run as MCP server
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="railway-reservation-system",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    else:
        # Run in standalone demo mode
        print("=== Railway Reservation System - Standalone Demo ===")
        print()
        
        # Sample input parameters
        train_name = "Rajdhani Express"
        travel_date = "2025-07-15"
        start_station = "New Delhi (NDLS)"
        end_station = "Mumbai Central (BCT)"
        travel_class = "AC2"
        
        print(f"Checking seat availability for:")
        print(f"Train: {train_name}")
        print(f"Date: {travel_date}")
        print(f"Route: {start_station} → {end_station}")
        print(f"Class: {travel_class}")
        print("-" * 50)
        
        # Get availability data
        availability = await check_seat_availability(
            train_name=train_name,
            travel_date=travel_date,
            start_station=start_station,
            end_station=end_station,
            travel_class=travel_class
        )
        
        # Print formatted JSON response
        print(json.dumps(availability, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
