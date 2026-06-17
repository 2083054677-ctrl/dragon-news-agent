#!/usr/bin/env python3
"""
龙虾新闻 Agent MCP Server
基于 stdin/stdout 的 JSON-RPC 工具服务，供 OpenClaw Agent 调用。
"""

import json
import sys
from tools import handle_tool_call, TOOLS_MANIFEST, sanitize_news_text


def send_response(response_id, result):
    """发送 JSON-RPC 响应"""
    response = {
        "jsonrpc": "2.0",
        "id": response_id,
        "result": result
    }
    output = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(output + "\n")
    sys.stdout.flush()


def send_error(response_id, code, message):
    """发送 JSON-RPC 错误响应"""
    response = {
        "jsonrpc": "2.0",
        "id": response_id,
        "error": {"code": code, "message": message}
    }
    output = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(output + "\n")
    sys.stdout.flush()


def handle_request(request):
    """处理单个 JSON-RPC 请求"""
    req_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params", {})

    if method == "initialize":
        return send_response(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {
                "name": "dragon-news-tools",
                "version": "1.0.0"
            }
        })

    elif method == "notifications/initialized":
        return  # 无需响应

    elif method == "tools/list":
        tools = []
        for tool in TOOLS_MANIFEST["tools"]:
            tools.append({
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": tool.get("parameters", {"type": "object", "properties": {}})
            })
        return send_response(req_id, {"tools": tools})

    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        result = handle_tool_call(tool_name, arguments)
        return send_response(req_id, {
            "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]
        })

    else:
        return send_error(req_id, -32601, f"Method not found: {method}")


def main():
    """MCP Server 主循环，监听 stdin"""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            handle_request(request)
        except json.JSONDecodeError as e:
            send_error(None, -32700, f"Parse error: {e}")
        except Exception as e:
            send_error(None, -32603, f"Internal error: {e}")


if __name__ == "__main__":
    main()
