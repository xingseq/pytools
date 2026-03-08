import asyncio
import time
import json
from concurrent.futures import ProcessPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import Any, Dict, AsyncGenerator
from core.base_tool import BaseTool
from core.schemas import ToolExecutionResult


class ToolExecutor:
    """工具执行器，支持超时控制和日志流式输出"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)
    
    async def execute_with_stream(
        self, 
        tool: BaseTool, 
        inputs: Dict[str, Any],
        timeout: int = 300
    ) -> AsyncGenerator[str, None]:
        """
        执行工具并流式返回日志
        
        Args:
            tool: 工具实例
            inputs: 输入参数
            timeout: 超时时间（秒）
            
        Yields:
            日志行（SSE格式）
        """
        start_time = time.time()
        
        # 发送开始日志 - 使用正确的JSON格式
        start_event = {
            "type": "log",
            "message": "开始执行工具..."
        }
        yield f"data: {json.dumps(start_event, ensure_ascii=False)}\n\n"
        
        try:
            # 在进程池中执行工具
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(self.executor, tool.run, inputs),
                timeout=timeout
            )
            
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            
            # 发送日志
            for log in result.logs:
                log_event = {
                    "type": "log",
                    "message": log
                }
                yield f"data: {json.dumps(log_event, ensure_ascii=False)}\n\n"
            
            # 发送结果
            if result.success:
                success_event = {
                    "type": "success",
                    "message": "执行成功",
                    "time": round(execution_time, 2)
                }
                yield f"data: {json.dumps(success_event, ensure_ascii=False)}\n\n"
            else:
                error_event = {
                    "type": "error",
                    "message": result.error
                }
                yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
            
            # 发送完成信号和结果
            complete_event = {
                "type": "complete",
                "result": result.model_dump()
            }
            yield f"data: {json.dumps(complete_event, ensure_ascii=False, default=str)}\n\n"
            
        except asyncio.TimeoutError:
            timeout_event = {
                "type": "error",
                "message": f"执行超时（{timeout}秒）"
            }
            yield f"data: {json.dumps(timeout_event, ensure_ascii=False)}\n\n"
            
            result = ToolExecutionResult(
                success=False,
                error=f"执行超时（{timeout}秒）",
                execution_time=timeout
            )
            
            complete_event = {
                "type": "complete",
                "result": result.model_dump()
            }
            yield f"data: {json.dumps(complete_event, ensure_ascii=False, default=str)}\n\n"
            
        except Exception as e:
            error_event = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
            
            result = ToolExecutionResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
            
            complete_event = {
                "type": "complete",
                "result": result.model_dump()
            }
            yield f"data: {json.dumps(complete_event, ensure_ascii=False, default=str)}\n\n"
    
    async def execute(
        self, 
        tool: BaseTool, 
        inputs: Dict[str, Any],
        timeout: int = 300
    ) -> ToolExecutionResult:
        """
        同步执行工具（不使用流式输出）
        
        Args:
            tool: 工具实例
            inputs: 输入参数
            timeout: 超时时间（秒）
            
        Returns:
            ToolExecutionResult
        """
        start_time = time.time()
        
        try:
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(self.executor, tool.run, inputs),
                timeout=timeout
            )
            result.execution_time = time.time() - start_time
            return result
            
        except asyncio.TimeoutError:
            return ToolExecutionResult(
                success=False,
                error=f"执行超时（{timeout}秒）",
                execution_time=timeout
            )
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def shutdown(self):
        """关闭执行器"""
        self.executor.shutdown(wait=True)