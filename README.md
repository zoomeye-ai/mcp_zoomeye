# ZoomEye MCP Server

A Model Context Protocol server that provides network asset information based on query conditions. This server allows LLMs to obtain network asset information and supports querying network asset information by zoomeye dork etc.

## Features

- Query ZoomEye for network asset information using dorks
- Caching mechanism to improve performance and reduce API calls
- Automatic retry mechanism for failed API requests
- Comprehensive error handling and logging

## Available Tools

- `zoomeye_search` - Get network asset information based on query conditions.
  - Required parameters:
    - `qbase64` (string): Base64 encoded query string for ZoomEye search
  - Optional parameters:
    - `page` (integer): View asset page number, default is 1
    - `pagesize` (integer): Number of records per page, default is 10, maximum is 1000
    - `fields` (string): The fields to return, separated by commas
    - `sub_type` (string): Data type, supports v4, v6, and web. Default is v4
    - `facets` (string): Statistical items, separated by commas if there are multiple
    - `ignore_cache` (boolean): Whether to ignore the cache

## Installation

### Using uv (Recommended)

No specific installation is required when using [`uv`](https://docs.astral.sh/uv/). We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-zoomeye*.

### Using PIP

Alternatively, you can install `mcp-server-zoomeye` via pip:

```bash
pip install mcp-server-zoomeye
```

After installation, you can run it as a script using the following command:

```bash
python -m mcp_server_zoomeye
```

## Configuration

### Configure Claude.app

Add the following in Claude settings:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "zoomeye": {
    "command": "uvx",
    "args": ["mcp-server-zoomeye"],
    "env": {
        "ZOOMEYE_API_KEY": "your_api_key_here"
    }
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
"mcpServers": {
  "zoomeye": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "-e", "ZOOMEYE_API_KEY=your_api_key_here", "mcp/zoomeye"],
    "env": {
      "ZOOMEYE_API_KEY": "your_api_key_here"
    }
  }
}
```
</details>

<details>
<summary>Installed via pip</summary>

```json
"mcpServers": {
  "zoomeye": {
    "command": "python",
    "args": ["-m", "mcp_server_zoomeye"],
    "env": {
        "ZOOMEYE_API_KEY": "your_api_key_here"
    }
  }
}
```
</details>

### Configure Zed

Add the following in Zed's settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "mcp-server-zoomeye": {
    "command": "uvx",
    "args": ["mcp-server-zoomeye"],
    "env": {
        "ZOOMEYE_API_KEY": "your_api_key_here"
    }
  }
],
```
</details>

<details>
<summary>Installed via pip</summary>

```json
"context_servers": {
  "mcp-server-zoomeye": {
    "command": "python",
    "args": ["-m", "mcp_server_zoomeye"],
    "env": {
        "ZOOMEYE_API_KEY": "your_api_key_here"
    }
  }
},
```
</details>

## API Documentation

### ZoomEye Search API

The ZoomEye Search API allows you to search for network assets using ZoomEye dorks. The API endpoint is `https://api.zoomeye.ai/v2/search`.


## Example Interaction

1. Retrieve global Apache Tomcat assets:
```json
{
  "name": "zoomeye_search",
  "arguments": {
    "qbase64": "app=\"Apache Tomcat\""
  }
}
```
Response:
```json
{
  "code": 60000,
  "message": "success",
  "total": 163139107,
  "query": "title=\"cisco vpn\"",
  "data": [
    {
      "url": "https://1.1.1.1:443",
      "ssl.jarm": "29d29d15d29d29d00029d29d29d29dea0f89a2e5fb09e4d8e099befed92cfa",
      "ssl.ja3s": "45094d08156d110d8ee97b204143db14",
      "iconhash_md5": "f3418a443e7d841097c714d69ec4bcb8",
      "robots_md5": "0b5ce08db7fb8fffe4e14d05588d49d9",
      "security_md5": "0b5ce08db7fb8fffe4e14d05588d49d9",
      "ip": "1.1.1.1",
      "domain": "www.google.com",
      "hostname": "SPACEX",
      "os": "windows",
      "port": 443,
      "service": "https",
      "title": ["GoogleGoogle appsGoogle Search"],
      "version": "1.1.0",
      "device": "webcam",
      "rdns": "c01031-001.cust.wallcloud.ch",
      "product": "OpenSSD",
      "header": "HTTP/1.1 302 Found Location: https://www.google.com/?gws_rd=ssl Cache-Control: private...",
      "header_hash": "27f9973fe57298c3b63919259877a84d",
      "body": "HTTP/1.1 302 Found Location: https://www.google.com/?gws_rd=ssl Cache-Control: private...",
      "body_hash": "84a18166fde3ee7e7c974b8d1e7e21b4",
      "banner": "SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3",
      "update_time": "2024-07-03T14:34:10",
      "header.server.name": "nginx",
      "header.server.version": "1.8.1",
      "continent.name": "Europe",
      "country.name": "Germany",
      "province.name": "Hesse",
      "city.name": "Frankfurt",
      "lon": "118.753262",
      "lat": "32.064838",
      "isp.name": "aviel.ru",
      "organization.name": "SERVISFIRST BANK",
      "zipcode": "210003",
      "idc": 0,
      "honeypot": 0,
      "asn": 4837,
      "protocol": "tcp",
      "ssl": "SSL Certificate Version: TLS 1.2 CipherSuit: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256...",
      "primary_industry": "Finance",
      "sub_industry": "bank",
      "rank": 60
    }
  ]
}
```

## Debugging

You can use the MCP inspector to debug the server. For uvx installation:

```bash
npx @modelcontextprotocol/inspector uvx mcp-server-zoomeye
```

Or if you have installed the package in a specific directory or are developing:

```bash
cd path/to/servers/src/mcp_server_zoomeye
npx @modelcontextprotocol/inspector uv run mcp-server-zoomeye
```

## Building

Docker Build:

```bash
docker build -t mcp/zoomeye .
```

## Contributing

We encourage contributions to mcp-server-zoomeye to help expand and improve its functionality. Whether it's adding new related tools, enhancing existing features, or improving documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see:
https://github.com/modelcontextprotocol/servers

Pull requests are welcome! Feel free to contribute new ideas, bug fixes, or enhancements to make mcp-server-zoomeye more robust and practical.

## License

mcp-server-zoomeye is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more information, see the LICENSE file in the project repository.
```