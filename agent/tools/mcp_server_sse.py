#!/usr/bin/env python3
"""
龙虾新闻 Agent MCP Server (SSE 传输)
基于 HTTP + SSE 的 MCP 工具服务，兼容 OpenClaw 的 MCP 实现。
"""

import json
import sys
import os
import threading
import uuid
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure tools module is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from tools import handle_tool_call, TOOLS_MANIFEST


class SSEMCPServer:
    """SSE-based MCP server using only Python stdlib."""

    def __init__(self, host="127.0.0.1", port=7700):
        self.host = host
        self.port = port
        self.sse_clients = []  # list of (queue, event_id)
        self.lock = threading.Lock()

    def send_sse(self, event_type, data, client_id=None):
        """Send an SSE event to all connected clients (or a specific one)."""
        with self.lock:
            for cid, queue in self.sse_clients:
                if client_id is None or cid == client_id:
                    queue.append((event_type, data))

    def start(self):
        server = self

        class MCPHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress HTTP log noise

            def do_GET(self):
                if self.path == "/sse":
                    self._handle_sse()
                elif self.path == "/health":
                    self._handle_health()
                else:
                    self.send_error(404)

            def do_POST(self):
                if self.path == "/messages":
                    self._handle_message()
                else:
                    self.send_error(404)

            def do_OPTIONS(self):
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def _handle_health(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode())

            def _handle_sse(self):
                client_id = str(uuid.uuid4())[:8]
                queue = []

                with server.lock:
                    server.sse_clients.append((client_id, queue))

                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                try:
                    # Send endpoint event telling client where to POST messages
                    endpoint_url = f"http://{server.host}:{server.port}/messages"
                    self.wfile.write(f"data: {json.dumps({'endpoint': endpoint_url})}\n\n".encode())
                    self.wfile.flush()

                    while True:
                        if queue:
                            event_type, data = queue.pop(0)
                            if event_type == "message":
                                self.wfile.write(f"event: message\ndata: {data}\n\n".encode())
                            else:
                                self.wfile.write(f"event: {event_type}\ndata: {data}\n\n".encode())
                            self.wfile.flush()
                        else:
                            time.sleep(0.1)
                            # Send keepalive comment
                            self.wfile.write(": keepalive\n\n".encode())
                            self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass
                finally:
                    with server.lock:
                        server.sse_clients = [(cid, q) for cid, q in server.sse_clients if cid != client_id]

            def _handle_message(self):
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length == 0:
                    self.send_error(400, "Empty body")
                    return

                raw_body = self.rfile.read(content_length)
                try:
                    request = json.loads(raw_body)
                except json.JSONDecodeError:
                    self.send_error(400, "Invalid JSON")
                    return

                req_id = request.get("id")
                method = request.get("method", "")
                params = request.get("params", {})

                try:
                    if method == "initialize":
                        result = {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {"listChanged": False}},
                            "serverInfo": {
                                "name": "dragon-news-tools",
                                "version": "1.0.0"
                            }
                        }
                    elif method == "notifications/initialized":
                        result = {}
                    elif method == "tools/list":
                        tools = []
                        for tool in TOOLS_MANIFEST["tools"]:
                            tools.append({
                                "name": tool["name"],
                                "description": tool["description"],
                                "inputSchema": tool.get("parameters", {"type": "object", "properties": {}})
                            })
                        result = {"tools": tools}
                    elif method == "tools/call":
                        tool_name = params.get("name", "")
                        arguments = params.get("arguments", {})
                        tool_result = handle_tool_call(tool_name, arguments)
                        result = {
                            "content": [{"type": "text", "text": json.dumps(tool_result, ensure_ascii=False)}]
                        }
                    else:
                        self.send_error(404, f"Method not found: {method}")
                        return

                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": result
                    }

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

                except Exception as e:
                    self.send_error(500, f"Internal error: {e}")

        print(f"🦞 MCP SSE Server starting on http://{self.host}:{self.port}")
        print(f"   SSE endpoint: http://{self.host}:{self.port}/sse")
        print(f"   Messages endpoint: http://{self.host}:{self.port}/messages")

        httpd = HTTPServer((self.host, self.port), MCPHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            httpd.shutdown()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7700
    host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
    server = SSEMCPServer(host=host, port=port)
    server.start()


if __name__ == "__main__":
    main()
