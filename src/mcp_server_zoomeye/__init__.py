from .server import serve


def main():
    """MCP ZoomEye Server - ZoomEye search for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to handle ZoomEye queries"
    )
    parser.add_argument("--key", type=str, help="ZoomEye API Key")

    args = parser.parse_args()
    asyncio.run(serve(args.key))


if __name__ == "__main__":
    main()