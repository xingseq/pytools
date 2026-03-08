#!/usr/bin/env python3
import subprocess
import sys
import os

# 切换到项目目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 使用poetry运行uvicorn
cmd = ["poetry", "run", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3020", "--reload"]

print(f"Starting server with command: {' '.join(cmd)}")
print(f"Server will be available at: http://localhost:3020")
print("Press Ctrl+C to stop")

try:
    subprocess.run(cmd)
except KeyboardInterrupt:
    print("\nServer stopped")
except Exception as e:
    print(f"Error starting server: {e}")
    sys.exit(1)