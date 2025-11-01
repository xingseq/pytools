import asyncio
import time
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
        
        yield f"data: {{'type': 'log', 'message': '开始执行工具...'}}\n\n"
        
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
                yield f"data: {{'type': 'log', 'message': {repr(log)}}}\n\n"
            
            # 发送结果
            if result.success:
                yield f"data: {{'type': 'success', 'message': '执行成功', 'time': {execution_time:.2f}}}\n\n"
            else:
                yield f"data: {{'type': 'error', 'message': {repr(result.error)}}}\n\n"
            
            # 发送完成信号和结果
            import json
            result_json = json.dumps(result.model_dump(), ensure_ascii=False, default=str)
            yield f"data: {{'type': 'complete', 'result': {result_json}}}\n\n"
            
        except asyncio.TimeoutError:
            yield f"data: {{'type': 'error', 'message': '执行超时（{timeout}秒）'}}\n\n"
            result = ToolExecutionResult(
                success=False,
                error=f"执行超时（{timeout}秒）",
                execution_time=timeout
            )
            import json
            result_json = json.dumps(result.model_dump(), ensure_ascii=False)
            yield f"data: {{'type': 'complete', 'result': {result_json}}}\n\n"
            
        except Exception as e:
            yield f"data: {{'type': 'error', 'message': {repr(str(e))}}}\n\n"
            result = ToolExecutionResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
            import json
            result_json = json.dumps(result.model_dump(), ensure_ascii=False)
            yield f"data: {{'type': 'complete', 'result': {result_json}}}\n\n"
    
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
