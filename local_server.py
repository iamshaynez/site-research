#!/usr/bin/env python3
"""
本地HTTP服务器脚本
用于托管public文件夹中的静态文件，便于本地调试
端口: 8080
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# 配置
PORT = 8080
PUBLIC_DIR = "public"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器，添加一些便于调试的功能"""
    
    def __init__(self, *args, **kwargs):
        # 设置服务目录为public文件夹
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)
    
    def end_headers(self):
        # 添加一些有用的HTTP头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    # 检查public目录是否存在
    if not os.path.exists(PUBLIC_DIR):
        print(f"错误: {PUBLIC_DIR} 目录不存在！")
        print(f"请确保在项目根目录运行此脚本，且存在 {PUBLIC_DIR} 文件夹")
        sys.exit(1)
    
    # 检查index.html是否存在
    index_path = os.path.join(PUBLIC_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"警告: {index_path} 不存在")
    
    # 显示public目录中的文件
    public_path = Path(PUBLIC_DIR)
    files = list(public_path.rglob("*"))
    print(f"\n📁 {PUBLIC_DIR} 目录内容:")
    for file_path in sorted(files)[:10]:  # 只显示前10个文件
        if file_path.is_file():
            relative_path = file_path.relative_to(public_path)
            print(f"  📄 {relative_path}")
    if len(files) > 10:
        print(f"  ... 还有 {len(files) - 10} 个文件")
    
    # 启动服务器
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"\n🚀 本地服务器已启动!")
            print(f"📍 服务地址: http://localhost:{PORT}")
            print(f"📁 服务目录: {os.path.abspath(PUBLIC_DIR)}")
            print(f"🔗 主页面: http://localhost:{PORT}/index.html")
            print(f"\n按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  服务器已停止")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"\n❌ 错误: 端口 {PORT} 已被占用")
            print(f"请先关闭占用端口 {PORT} 的程序，或修改脚本中的端口号")
        else:
            print(f"\n❌ 服务器启动失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 未知错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 50)
    print("🌐 本地HTTP服务器 - 用于调试静态网站")
    print("=" * 50)
    main()
