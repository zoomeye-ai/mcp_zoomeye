import os
from enum import Enum
import json
import requests
from typing import Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError

class ZoomeyeTools(str, Enum):
    ZOOMEYE_SEARCH = "zoomeye_search"
    """Search query for ZoomEye."""

def zoomeye_search(qbase64: str, page: int = 1, pagesize: int = 10, fields: str = "", sub_type: str = "", facets: str = "", ignore_cache: bool = False):
    """Search query for ZoomEye.
    ### Parameters
    |Parameter|Type|Required|Description|
    | ----- | ----- | ----- | ----- |
    |qbase64|string|true|Base64 encoded query string. For more, refer to Related references.|
    |fields|string|false|The fields to return, separated by commas. Default: ip, port, domain, update_time. For more, refer to Response field description|
    |sub\_type|string|false|Data type, supports v4, v6, and web. Default is v4.|
    |page|integer|false|View asset page number|
    |pagesize|integer|false|Number of records per page, default is 10, maximum is 10,000.|
    |facets|string|false|Statistical items, separated by commas if there are multiple. Supports country, subdivisions, city, product, service, device, OS, and port.|
    |ignore\_cache|boolean|false|Whether to ignore the cache. false, supported by Business plan and above.|
    """
    service = ZoomeyeService()
    return service.query(
        qbase64=qbase64,
        page=page,
        pagesize=pagesize,
        fields=fields,
        sub_type=sub_type,
        facets=facets,
        ignore_cache=ignore_cache
    )


class ZoomeyeService:
    def __init__(self, key: Optional[str] = None):
        self.key = key
        if not self.key:
            self.key = os.getenv("ZOOMEYE_API_KEY")
    
    def query(self, qbase64, page=1, pagesize=10, fields=None, sub_type=None, facets=None, ignore_cache=None):
        """Query ZoomEye API with the given parameters.
        
        Args:
            qbase64 (str): Base64 encoded query string.
            page (int, optional): Page number. Defaults to 1.
            pagesize (int, optional): Number of records per page. Defaults to 10.
            fields (str, optional): Fields to return, comma separated. Defaults to None.
            sub_type (str, optional): Data type (v4, v6, web). Defaults to None.
            facets (str, optional): Statistical items, comma separated. Defaults to None.
            ignore_cache (bool, optional): Whether to ignore cache. Defaults to None.
            
        Returns:
            dict: The API response data.
            
        Raises:
            ValueError: If API key is not provided or API request fails.
        """
        if not self.key:
            raise ValueError("ZoomEye API key is required. Please set it via environment variable ZOOMEYE_API_KEY or pass it to the constructor.")
        
        url = "https://api.zoomeye.ai/v2/search"
        headers = {"API-KEY": self.key, "Content-Type": "application/json"}
        
        # Prepare request data
        data = {"qbase64": qbase64, "page": page, "pagesize": pagesize}
        
        # Add optional parameters if provided
        if fields:
            data["fields"] = fields
        if sub_type:
            data["sub_type"] = sub_type
        if facets:
            data["facets"] = facets
        if ignore_cache is not None:
            data["ignore_cache"] = ignore_cache
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error querying ZoomEye API: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from ZoomEye API")



async def serve(key: str | None = None) -> None:
    server = Server("mcp-zoomeye")
    zoomeye_service = ZoomeyeService(key=key)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """Tool list"""
        return [
            Tool(
                name=ZoomeyeTools.ZOOMEYE_SEARCH,
                description="Get network asset information based on query conditions.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "qbase64": {
                            "type": "string",
                            "description": "Base64 encoded query string for ZoomEye search",
                        },
                        "page": {
                            "type": "integer",
                            "description": "View asset page number, default is 1",
                            "default": 1
                        },
                        "pagesize": {
                            "type": "integer",
                            "description": "Number of records per page, default is 10, maximum is 1000",
                            "default": 10,
                            "maximum": 1000
                        },
                        "fields": {
                            "type": "string",
                            "description": "The fields to return, separated by commas. Default: ip, port, domain, update_time"
                        },
                        "sub_type": {
                            "type": "string",
                            "description": "Data type, supports v4, v6, and web. Default is v4",
                            "enum": ["v4", "v6", "web"]
                        },
                        "facets": {
                            "type": "string",
                            "description": "Statistical items, separated by commas if there are multiple. Supports country, subdivisions, city, product, service, device, OS, and port"
                        },
                        "ignore_cache": {
                            "type": "boolean",
                            "description": "Whether to ignore the cache. Supported by Business plan and above"
                        }
                    },
                    "required": ["qbase64"],
                },
            )
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for zoomeye queries."""
        try:
            match name:
                case ZoomeyeTools.ZOOMEYE_SEARCH:
                    qbase64 = arguments.get("qbase64")
                    if not qbase64:
                        raise ValueError("Missing required argument: qbase64")

                    page = arguments.get("page", 1)
                    pagesize = arguments.get("pagesize", 10)
                    fields = arguments.get("fields")
                    sub_type = arguments.get("sub_type")
                    facets = arguments.get("facets")
                    ignore_cache = arguments.get("ignore_cache")

                    result = zoomeye_service.query(
                        qbase64=qbase64,
                        page=page,
                        pagesize=pagesize,
                        fields=fields,
                        sub_type=sub_type,
                        facets=facets,
                        ignore_cache=ignore_cache
                    )
                case _:
                    raise ValueError(f"Unknown tool: {name}")

            formatted_result = json.dumps(result, ensure_ascii=False, indent=2)
            return [
                TextContent(type="text", text=formatted_result if result is not None else "")
            ]

        except Exception as e:
            raise ValueError(f"Error processing mcp-server-zoomeye query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)



if __name__ == "__main__":
    import base64
    import sys
    
    zoomeye_service = ZoomeyeService()
    try:
        query = 'app="Apache Tomcat"'
        qbase64 = base64.b64encode(query.encode()).decode()
        result = zoomeye_service.query(qbase64=qbase64, page=1, pagesize=5)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as e:
        print(f"{e}", file=sys.stderr)
        print("ZoomEye API key is required. Please set it via environment variable ZOOMEYE_API_KEY or --key set value.", file=sys.stderr)