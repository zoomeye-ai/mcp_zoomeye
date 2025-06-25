import json
import os
from enum import Enum
from typing import Optional, Sequence
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource, Prompt, PromptArgument
import httpx
from .prompts import SEARCH_SYNTAX_GUIDE

load_dotenv()


class ZoomeyeTools(str, Enum):
    ZOOMEYE_SEARCH = "zoomeye_search"
    """Search query for ZoomEye."""
    ZOOMEYE_VULDB_BY_ID = "zoomeye_vuldb_by_id"
    """Query vulnerability by ID."""

    ZOOMEYE_VULDB_BY_KEYWORD = "zoomeye_vuldb_by_keyword"
    """Query vulnerability by keyword."""


def zoomeye_search(qbase64: str, page: int = 1, pagesize: int = 10, fields: str = "", sub_type: str = "",
                   facets: str = "", ignore_cache: bool = False):
    """Search query for ZoomEye.
    ### Parameters
    |Parameter|Type|Required|Description|
    | ----- | ----- | ----- | ----- |
    |qbase64|string|true|Base64 encoded query string. For more, refer to Related references.|
    |fields|string|false|The fields to return, separated by commas. Default: ip, port, domain, update_time. For more, refer to Response field description|
    |sub_type|string|false|Data type, supports v4, v6, and web. Default is v4.|
    |page|integer|false|View asset page number|
    |pagesize|integer|false|Number of records per page, default is 10, maximum is 10,000.|
    |facets|string|false|Statistical items, separated by commas if there are multiple. Supports country, subdivisions, city, product, service, device, OS, and port.|
    |ignore_cache|boolean|false|Whether to ignore the cache. false, supported by Business plan and above.|
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


def zoomeye_query_vuldb_by_id(cve_id: str):
    """Search for vulnerabilities by ID. eg: CVE-XXXX-XXXX,CNVD-XXXX-XXXX,CNNVD-XXXX-XXXX"""
    service = ZoomeyeService()
    return service.query_vulnerability_by_id(cve_id)


class ZoomeyeService:
    def __init__(self, key: Optional[str] = None):
        self.key = key
        if not self.key:
            self.key = os.getenv("ZOOMEYE_API_KEY")

    async def get_client(self):
        proxies = None
        https_proxy = os.getenv("https_proxy")
        http_proxy = os.getenv("http_proxy")
        if https_proxy or http_proxy:
            proxies = {}
            if https_proxy:
                proxies["https://"] = https_proxy
            if http_proxy:
                proxies["http://"] = http_proxy
        return httpx.AsyncClient(proxies=proxies)

    async def query(self, qbase64, page=1, pagesize=10, fields=None, sub_type=None, facets=None, ignore_cache=None):
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
            raise ValueError(
                "ZoomEye API key is required. Please set it via environment variable ZOOMEYE_API_KEY or pass it to the constructor.")

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
            client = await self.get_client()
            async with client:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()  # Raise exception for HTTP errors
                return response.json()
        except httpx.HTTPError as e:
            raise ValueError(f"Error querying ZoomEye API: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from ZoomEye API")

    async def query_vulnerability_by_id(self, cve_id: str):
        """Query vulnerability by ID.
        Args:
            cve_id (str): The CVE ID to query.
        Returns:
            dict: The API response data.
        Raises:
            ValueError: If API key is not provided or API request fails.
        """
        url = "https://api.zoomeye.ai/v2/vuldb/{}".format(cve_id)
        headers = {"API-KEY": self.key, "Content-Type": "application/json"}
        try:
            client = await self.get_client()
            async with client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  # Raise exception for HTTP errors
                return response.json()
        except httpx.HTTPError as e:
            raise ValueError(f"Error querying ZoomEye API: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from ZoomEye API")

    async def query_vulnerability_by_keyword(self, keyword: str, page_size: int = 10):
        """Query vulnerability by keyword.
        Args:
            keyword (str): The keyword to query. 
        Returns:
            dict: The API response data.
        Raises:
            ValueError: If API key is not provided or API request fails.
        """
        url = "https://api.zoomeye.ai/v2/search/vuldb"
        headers = {"API-KEY": self.key, "Content-Type": "application/json"}
        try:
            client = await self.get_client()
            async with client:
                response = await client.get(url, headers=headers, params={"search": keyword, "page_size": page_size})
                response.raise_for_status()  # Raise exception for HTTP errors
                return response.json()
        except httpx.HTTPError as e:
            import traceback
            traceback.print_exc()
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
                description=SEARCH_SYNTAX_GUIDE,
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
            ),
            Tool(
                name=ZoomeyeTools.ZOOMEYE_VULDB_BY_ID,
                description="""Search for detailed vulnerability information by vulnerability ID and return formatted results.

    Use this tool to retrieve comprehensive security vulnerability details from the vulnerability
    database using a vulnerability identifier (CVE, CNVD, CNNVD). Results include:""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cve_id": {
                            "type": "string",
                            "description": "A valid vulnerability identifier, eg: CVE-XXXX-XXXX,CNVD-XXXX-XXXX,CNNVD-XXXX-XXXX",
                        }
                    },
                    "required": ["cve_id"],
                },
            ),
            Tool(
                name=ZoomeyeTools.ZOOMEYE_VULDB_BY_KEYWORD,
                description="""Search ZoomEye's vulnerability database for security vulnerabilities based on a specified keyword.

    This function queries the ZoomEye vulnerability database to retrieve information about known
    security vulnerabilities associated with specific products, vendors.
    Results include vulnerability details such as CVE IDs, severity ratings, affected versions,
    and vulnerability descriptions.""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": """Search term to query the vulnerability database. This can be a product name,
                      vendor name (e.g., "nginx", "mysql", "tomcat",
                      "WordPress", "hikvision", "huawei").""",
                        },
                        "page_size": {
                            "type": "integer",
                            "description": "Number of records per page, default is 10, maximum is 100.",
                            "default": 10,
                            "maximum": 100
                        }
                    },
                    "required": ["keyword"],
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

                    result = await zoomeye_service.query(
                        qbase64=qbase64,
                        page=page,
                        pagesize=pagesize,
                        fields=fields,
                        sub_type=sub_type,
                        facets=facets,
                        ignore_cache=ignore_cache
                    )
                case ZoomeyeTools.ZOOMEYE_VULDB_BY_ID:
                    cve_id = arguments.get("cve_id")
                    if not cve_id:
                        raise ValueError("Missing required argument: cve_id")
                    result = await zoomeye_service.query_vulnerability_by_id(cve_id)
                case ZoomeyeTools.ZOOMEYE_VULDB_BY_KEYWORD:
                    keyword = arguments.get("keyword")
                    if not keyword:
                        raise ValueError("Missing required argument: keyword")
                    result = await zoomeye_service.query_vulnerability_by_keyword(keyword)
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
