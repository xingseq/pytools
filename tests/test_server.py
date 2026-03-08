"""
测试服务器端点和应用
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestServer:
    """测试服务器基本功能"""
    
    def setup_method(self):
        """每个测试方法前执行"""
        self.client = TestClient(app)
    
    def test_app_import(self):
        """测试应用可以导入"""
        assert app is not None
        assert app.title == "PyTools API"
    
    def test_root_endpoint(self):
        """测试根端点"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_api_docs_endpoints(self):
        """测试API文档端点"""
        # 测试OpenAPI文档
        response = self.client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        
        # 测试OpenAPI JSON
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
    
    def test_tools_list_endpoint(self):
        """测试工具列表端点"""
        response = self.client.get("/api/tools")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 应该至少有3个工具
        assert len(data) >= 3
        
        # 验证每个工具的结构
        for tool in data:
            assert "id" in tool
            assert "name" in tool
            assert "description" in tool
            assert "category" in tool
            assert "input_fields" in tool
    
    def test_tool_detail_endpoint(self):
        """测试工具详情端点"""
        tool_ids = ["image_resize", "image_split", "text_transform"]
        
        for tool_id in tool_ids:
            response = self.client.get(f"/api/tool/{tool_id}")
            assert response.status_code == 200, f"工具 {tool_id} 详情请求失败"
            data = response.json()
            assert data["id"] == tool_id
            assert "name" in data
            assert "description" in data
            assert "input_fields" in data
    
    def test_nonexistent_tool_detail(self):
        """测试不存在的工具详情"""
        response = self.client.get("/api/tool/nonexistent")
        assert response.status_code == 404
    
    def test_history_endpoint(self):
        """测试历史记录端点"""
        response = self.client.get("/api/history")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 历史记录可能为空，但应该是列表


class TestTextTransformToolAPI:
    """测试文本转换工具的API端点"""
    
    def setup_method(self):
        """每个测试方法前执行"""
        self.client = TestClient(app)
    
    def test_text_transform_execute_uppercase(self):
        """测试文本转大写操作"""
        form_data = {
            "text": "hello world",
            "operation": "转大写"
        }
        
        response = self.client.post(
            "/api/tool/text_transform/execute",
            data=form_data,
            headers={"Accept": "text/event-stream"}
        )
        
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")
        
        # 解析SSE流
        events = []
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    import json
                    try:
                        event_data = json.loads(line_str[6:])
                        events.append(event_data)
                    except json.JSONDecodeError:
                        pass
        
        # 应该至少有一个包含结果的事件
        assert len(events) > 0
        
        # 查找包含结果的事件
        result_event = None
        for event in events:
            if event.get("type") == "result":
                result_event = event
                break
        
        assert result_event is not None
        assert result_event.get("success") is True
        assert "HELLO WORLD" in result_event.get("output", "")
    
    def test_text_transform_execute_missing_field(self):
        """测试缺少必需字段"""
        form_data = {
            "operation": "转大写"
            # 缺少text字段
        }
        
        response = self.client.post(
            "/api/tool/text_transform/execute",
            data=form_data
        )
        
        # 应该返回错误
        assert response.status_code == 422  # 验证错误


if __name__ == "__main__":
    pytest.main([__file__])