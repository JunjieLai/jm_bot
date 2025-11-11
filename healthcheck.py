#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的健康检查 HTTP 服务器
在后台运行，让 Railway 知道服务还活着
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import logging

logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """健康检查处理器"""

    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """禁用访问日志"""
        pass


def start_healthcheck_server(port=8080):
    """启动健康检查服务器（在后台线程中）"""
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        logger.info(f"健康检查服务器启动在端口 {port}")
        return server
    except Exception as e:
        logger.warning(f"无法启动健康检查服务器: {e}")
        return None
