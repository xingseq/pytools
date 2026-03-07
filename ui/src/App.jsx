import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  Scissors, 
  Type, 
  Settings, 
  Play, 
  FileText, 
  Download,
  AlertCircle,
  CheckCircle,
  Loader,
  Image as ImageIcon
} from 'lucide-react';

// API基础URL - 使用相对路径，由星序框架代理
const API_BASE_URL = '';

// 工具定义 - 与后端tools目录中的工具匹配
const TOOLS = [
  {
    id: 'image_resize',
    name: '图像缩放',
    description: '调整图片尺寸，支持按比例或指定宽高',
    icon: <Settings className="w-5 h-5" />,
    category: '图像处理',
    inputFields: [
      {
        name: 'image',
        label: '上传图片',
        type: 'file',
        required: true,
        accept: 'image/*',
        helpText: '支持 JPG, PNG, GIF 等格式'
      },
      {
        name: 'mode',
        label: '缩放模式',
        type: 'select',
        required: true,
        options: ['按比例', '指定宽度', '指定高度', '指定宽高'],
        default: '按比例'
      },
      {
        name: 'scale',
        label: '缩放比例 (%)',
        type: 'number',
        required: false,
        default: 50,
        min: 1,
        max: 1000,
        condition: { field: 'mode', value: '按比例' }
      },
      {
        name: 'width',
        label: '宽度 (像素)',
        type: 'number',
        required: false,
        min: 1,
        condition: { field: 'mode', value: ['指定宽度', '指定宽高'] }
      },
      {
        name: 'height',
        label: '高度 (像素)',
        type: 'number',
        required: false,
        min: 1,
        condition: { field: 'mode', value: ['指定高度', '指定宽高'] }
      }
    ]
  },
  {
    id: 'image_split',
    name: '图片切分',
    description: '将大图片按指定方式切分成多个小图片',
    icon: <Scissors className="w-5 h-5" />,
    category: '图像处理',
    inputFields: [
      {
        name: 'image',
        label: '上传图片',
        type: 'file',
        required: true,
        accept: 'image/*',
        helpText: '支持 JPG, PNG, GIF 等格式'
      },
      {
        name: 'split_method',
        label: '切分方式',
        type: 'select',
        required: true,
        options: ['按行列数切分', '按固定尺寸切分'],
        default: '按行列数切分'
      },
      {
        name: 'rows',
        label: '行数',
        type: 'number',
        required: false,
        default: 2,
        min: 1,
        max: 50,
        condition: { field: 'split_method', value: '按行列数切分' }
      },
      {
        name: 'cols',
        label: '列数',
        type: 'number',
        required: false,
        default: 2,
        min: 1,
        max: 50,
        condition: { field: 'split_method', value: '按行列数切分' }
      },
      {
        name: 'slice_width',
        label: '切片宽度(像素)',
        type: 'number',
        required: false,
        min: 10,
        condition: { field: 'split_method', value: '按固定尺寸切分' }
      },
      {
        name: 'slice_height',
        label: '切片高度(像素)',
        type: 'number',
        required: false,
        min: 10,
        condition: { field: 'split_method', value: '按固定尺寸切分' }
      },
      {
        name: 'output_format',
        label: '输出格式',
        type: 'select',
        required: true,
        options: ['PNG', 'JPG', '与原图相同'],
        default: 'PNG'
      }
    ]
  },
  {
    id: 'text_transform',
    name: '文本转换',
    description: '对文本进行大小写转换、反转、去重等操作',
    icon: <Type className="w-5 h-5" />,
    category: '文本处理',
    inputFields: [
      {
        name: 'text',
        label: '输入文本',
        type: 'textarea',
        required: true,
        placeholder: '请输入要处理的文本...',
        rows: 6
      },
      {
        name: 'operation',
        label: '操作类型',
        type: 'select',
        required: true,
        options: ['转大写', '转小写', '反转', '去除空格', '统计字数'],
        default: '转大写'
      }
    ]
  }
];

function App() {
  const [selectedTool, setSelectedTool] = useState(TOOLS[0]);
  const [formData, setFormData] = useState({});
  const [previewFile, setPreviewFile] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [logs, setLogs] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // 初始化表单数据
  useEffect(() => {
    const initialData = {};
    selectedTool.inputFields.forEach(field => {
      if (field.default !== undefined) {
        initialData[field.name] = field.default;
      }
    });
    setFormData(initialData);
    setPreviewFile(null);
    setLogs([]);
    setResult(null);
    setError(null);
  }, [selectedTool]);

  // 检查字段是否应该显示
  const shouldShowField = (field) => {
    if (!field.condition) return true;
    
    const { field: conditionField, value } = field.condition;
    const fieldValue = formData[conditionField];
    
    if (Array.isArray(value)) {
      return value.includes(fieldValue);
    }
    return fieldValue === value;
  };

  // 处理表单输入变化
  const handleInputChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  // 处理文件上传
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setPreviewFile({
        name: file.name,
        size: (file.size / 1024).toFixed(2) + ' KB',
        type: file.type
      });
      
      // 创建File对象用于FormData
      handleInputChange('image', file);
    }
  };

  // 执行工具
  const executeTool = async () => {
    setIsExecuting(true);
    setLogs([]);
    setResult(null);
    setError(null);

    try {
      const formDataToSend = new FormData();
      
      // 添加表单数据
      Object.entries(formData).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          // 如果是文件对象，直接添加
          if (value instanceof File) {
            formDataToSend.append(key, value);
          } else {
            formDataToSend.append(key, String(value));
          }
        }
      });

      // 使用SSE流式执行
      const response = await fetch(`${API_BASE_URL}/api/tool/${selectedTool.id}/execute`, {
        method: 'POST',
        body: formDataToSend
      });

      if (!response.ok) {
        throw new Error(`API请求失败: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.substring(6);
            try {
              const data = JSON.parse(dataStr);
              
              if (data.type === 'log') {
                setLogs(prev => [...prev, data.message]);
              } else if (data.type === 'complete') {
                setResult(data.result);
              } else if (data.type === 'error') {
                setError(data.message);
              }
            } catch (e) {
              console.error('解析SSE数据失败:', e, dataStr);
            }
          }
        }
      }
      
    } catch (err) {
      setError(err.message);
      setLogs(prev => [...prev, `❌ 错误: ${err.message}`]);
    } finally {
      setIsExecuting(false);
    }
  };

  // 下载结果文件
  const downloadFile = (filename) => {
    const url = `${API_BASE_URL}/outputs/${filename}`;
    window.open(url, '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        {/* 顶部标题 */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
            <ImageIcon className="w-8 h-8 text-blue-600" />
            Python工具集 - 图像处理与文本转换
          </h1>
          <p className="text-gray-600 mt-2">
            提供图像缩放、图片切分和文本转换等实用工具
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* 左侧工具栏 */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-4">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">工具列表</h2>
            <div className="space-y-2">
              {TOOLS.map(tool => (
                <button
                  key={tool.id}
                  onClick={() => setSelectedTool(tool)}
                  className={`w-full text-left p-3 rounded-lg transition-all ${
                    selectedTool.id === tool.id
                      ? 'bg-blue-50 border border-blue-200 text-blue-700'
                      : 'hover:bg-gray-50 text-gray-600'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-md ${
                      selectedTool.id === tool.id ? 'bg-blue-100' : 'bg-gray-100'
                    }`}>
                      {tool.icon}
                    </div>
                    <div>
                      <div className="font-medium">{tool.name}</div>
                      <div className="text-xs text-gray-500 mt-1">{tool.description}</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>

            {/* 当前工具信息 */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">当前工具</h3>
              <div className="bg-blue-50 p-3 rounded-lg">
                <div className="flex items-center gap-2 text-blue-700">
                  {selectedTool.icon}
                  <span className="font-medium">{selectedTool.name}</span>
                </div>
                <p className="text-sm text-blue-600 mt-2">{selectedTool.description}</p>
                <div className="mt-2">
                  <span className="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                    {selectedTool.category}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* 主内容区 */}
          <div className="lg:col-span-3 space-y-6">
            {/* 表单区域 */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-6">参数设置</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {selectedTool.inputFields
                  .filter(shouldShowField)
                  .map(field => (
                    <div 
                      key={field.name} 
                      className={field.type === 'textarea' ? 'md:col-span-2' : ''}
                    >
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        {field.label}
                        {field.required && <span className="text-red-500 ml-1">*</span>}
                      </label>
                      
                      {field.type === 'select' ? (
                        <select
                          value={formData[field.name] || field.default || ''}
                          onChange={(e) => handleInputChange(field.name, e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                          {field.options.map(option => (
                            <option key={option} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      ) : field.type === 'textarea' ? (
                        <textarea
                          value={formData[field.name] || ''}
                          onChange={(e) => handleInputChange(field.name, e.target.value)}
                          placeholder={field.placeholder}
                          rows={field.rows || 4}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
                        />
                      ) : field.type === 'file' ? (
                        <div className="space-y-3">
                          <div className="flex items-center gap-3">
                            <label className="flex-1">
                              <div className="cursor-pointer border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-500 transition-colors">
                                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                                <div className="text-sm text-gray-600">
                                  点击选择文件或拖放文件到这里
                                </div>
                                <input
                                  type="file"
                                  onChange={handleFileUpload}
                                  accept={field.accept}
                                  className="hidden"
                                />
                              </div>
                            </label>
                          </div>
                          
                          {previewFile && (
                            <div className="bg-gray-50 p-3 rounded-lg">
                              <div className="flex items-center gap-3">
                                <FileText className="w-5 h-5 text-green-600" />
                                <div className="flex-1">
                                  <div className="font-medium text-sm">{previewFile.name}</div>
                                  <div className="text-xs text-gray-500">
                                    {previewFile.size} · {previewFile.type}
                                  </div>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      ) : field.type === 'number' ? (
                        <input
                          type="number"
                          value={formData[field.name] || field.default || ''}
                          onChange={(e) => handleInputChange(field.name, e.target.value)}
                          min={field.min}
                          max={field.max}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                      ) : (
                        <input
                          type="text"
                          value={formData[field.name] || ''}
                          onChange={(e) => handleInputChange(field.name, e.target.value)}
                          placeholder={field.placeholder}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                      )}
                      
                      {field.helpText && (
                        <p className="mt-1 text-xs text-gray-500">{field.helpText}</p>
                      )}
                    </div>
                  ))}
              </div>

              {/* 执行按钮 */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <button
                  onClick={executeTool}
                  disabled={isExecuting}
                  className={`inline-flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
                    isExecuting
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {isExecuting ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      执行中...
                    </>
                  ) : (
                    <>
                      <Play className="w-5 h-5" />
                      执行工具
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* 输出区域 */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">执行输出</h2>
              
              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <h3 className="font-medium text-red-800">执行错误</h3>
                      <p className="text-red-600 mt-1">{error}</p>
                    </div>
                  </div>
                </div>
              )}

              {result && (
                <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <h3 className="font-medium text-green-800">执行成功</h3>
                      <pre className="mt-2 text-green-700 whitespace-pre-wrap bg-green-100 p-3 rounded text-sm">
                        {result.output || JSON.stringify(result, null, 2)}
                      </pre>
                      
                      {result.files && result.files.length > 0 && (
                        <div className="mt-3">
                          <h4 className="text-sm font-medium text-green-800 mb-2">生成文件:</h4>
                          <div className="space-y-2">
                            {result.files.map((file, index) => (
                              <div key={index} className="flex items-center justify-between bg-green-100 p-3 rounded">
                                <div className="flex items-center gap-3">
                                  <FileText className="w-4 h-4 text-green-700" />
                                  <span className="text-sm text-green-800">{file.name}</span>
                                </div>
                                <button
                                  onClick={() => downloadFile(file.name)}
                                  className="text-xs bg-green-200 hover:bg-green-300 text-green-800 px-3 py-1 rounded transition-colors flex items-center gap-1"
                                >
                                  <Download className="w-3 h-3" />
                                  下载
                                </button>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* 日志输出 */}
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                  <h3 className="text-sm font-medium text-gray-700">执行日志</h3>
                </div>
                <div className="h-64 overflow-y-auto bg-gray-900 p-4">
                  {logs.length === 0 ? (
                    <div className="text-gray-500 italic text-sm">
                      暂无日志，执行工具后日志将显示在这里...
                    </div>
                  ) : (
                    <div className="font-mono text-sm space-y-1">
                      {logs.map((log, index) => (
                        <div key={index} className="text-gray-300">
                          <span className="text-gray-500">[{new Date().toLocaleTimeString()}]</span>{' '}
                          {log}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 页脚 */}
        <footer className="mt-8 pt-6 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>Python工具集 v1.0.0 · 星序引擎子应用</p>
          <p className="mt-1">后端API: FastAPI + Python · 前端: React + Tailwind CSS</p>
        </footer>
      </div>
    </div>
  );
}

export default App;