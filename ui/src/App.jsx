import React, { useState } from 'react';
import { 
  Code2, 
  Settings, 
  Package, 
  Cpu, 
  Play, 
  CheckCircle, 
  AlertCircle,
  Terminal,
  FileCode,
  FolderOpen,
  Zap
} from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('format');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  
  // 格式化相关状态
  const [formatPath, setFormatPath] = useState('');
  const [formatter, setFormatter] = useState('black');
  
  // 代码检查相关状态
  const [lintPath, setLintPath] = useState('');
  const [linter, setLinter] = useState('pylint');
  
  // 依赖管理相关状态
  const [depAction, setDepAction] = useState('list');
  const [packageName, setPackageName] = useState('');
  
  // 虚拟环境相关状态
  const [venvAction, setVenvAction] = useState('list');
  const [venvName, setVenvName] = useState('');
  
  // 执行脚本相关状态
  const [scriptPath, setScriptPath] = useState('');
  const [scriptArgs, setScriptArgs] = useState('');

  const tabs = [
    { id: 'format', name: '代码格式化', icon: Code2, color: 'text-blue-500' },
    { id: 'lint', name: '代码检查', icon: CheckCircle, color: 'text-green-500' },
    { id: 'deps', name: '依赖管理', icon: Package, color: 'text-yellow-500' },
    { id: 'venv', name: '虚拟环境', icon: Cpu, color: 'text-purple-500' },
    { id: 'run', name: '执行脚本', icon: Play, color: 'text-red-500' },
    { id: 'terminal', name: '终端输出', icon: Terminal, color: 'text-gray-500' },
  ];

  const handleExecute = async () => {
    setLoading(true);
    setOutput('');
    
    try {
      // 这里应该调用实际的API
      // 暂时模拟API调用
      setTimeout(() => {
        let result = '';
        
        switch (activeTab) {
          case 'format':
            result = `✅ 格式化完成\n工具: ${formatter}\n路径: ${formatPath}\n\n使用命令: ${formatter === 'black' ? 'black' : 'autopep8 --in-place --aggressive'} ${formatPath}`;
            break;
          case 'lint':
            result = `🔍 代码检查完成\n工具: ${linter}\n路径: ${lintPath}\n\n检查结果: 代码质量良好，无严重问题`;
            break;
          case 'deps':
            result = `📦 依赖${depAction}操作完成\n包名: ${packageName || '无'}\n\n当前环境Python包:\n• numpy==1.24.3\n• pandas==2.0.3\n• matplotlib==3.7.2`;
            break;
          case 'venv':
            result = `🐍 虚拟环境${venvAction}操作完成\n环境名称: ${venvName || '无'}\n\n可用虚拟环境:\n• venv/\n• myenv/\n• test_env/`;
            break;
          case 'run':
            result = `▶️ 执行脚本完成\n脚本: ${scriptPath}\n参数: ${scriptArgs || '无'}\n\n输出:\nHello from Python!`;
            break;
          default:
            result = '请选择一个功能';
        }
        
        setOutput(result);
        setLoading(false);
      }, 1000);
    } catch (error) {
      setOutput(`❌ 错误: ${error.message}`);
      setLoading(false);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'format':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">文件或目录路径</label>
              <div className="flex">
                <input
                  type="text"
                  value={formatPath}
                  onChange={(e) => setFormatPath(e.target.value)}
                  className="flex-grow p-3 border rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="例如: ./src/ 或 ./main.py"
                />
                <button className="bg-gray-100 px-4 rounded-r-lg border border-l-0">
                  <FolderOpen className="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">格式化工具</label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setFormatter('black')}
                  className={`p-4 border rounded-lg flex flex-col items-center ${
                    formatter === 'black' 
                    ? 'border-blue-500 bg-blue-50 text-blue-700' 
                    : 'hover:bg-gray-50'
                  }`}
                >
                  <Code2 className="w-8 h-8 mb-2" />
                  <span className="font-semibold">Black</span>
                  <span className="text-sm text-gray-600 mt-1">代码格式化</span>
                </button>
                
                <button
                  onClick={() => setFormatter('autopep8')}
                  className={`p-4 border rounded-lg flex flex-col items-center ${
                    formatter === 'autopep8' 
                    ? 'border-blue-500 bg-blue-50 text-blue-700' 
                    : 'hover:bg-gray-50'
                  }`}
                >
                  <Settings className="w-8 h-8 mb-2" />
                  <span className="font-semibold">Autopep8</span>
                  <span className="text-sm text-gray-600 mt-1">PEP8 格式化</span>
                </button>
              </div>
            </div>
          </div>
        );
        
      case 'lint':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">文件或目录路径</label>
              <div className="flex">
                <input
                  type="text"
                  value={lintPath}
                  onChange={(e) => setLintPath(e.target.value)}
                  className="flex-grow p-3 border rounded-l-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  placeholder="例如: ./src/ 或 ./main.py"
                />
                <button className="bg-gray-100 px-4 rounded-r-lg border border-l-0">
                  <FolderOpen className="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">代码检查工具</label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setLinter('pylint')}
                  className={`p-4 border rounded-lg flex flex-col items-center ${
                    linter === 'pylint' 
                    ? 'border-green-500 bg-green-50 text-green-700' 
                    : 'hover:bg-gray-50'
                  }`}
                >
                  <AlertCircle className="w-8 h-8 mb-2" />
                  <span className="font-semibold">Pylint</span>
                  <span className="text-sm text-gray-600 mt-1">全面代码分析</span>
                </button>
                
                <button
                  onClick={() => setLinter('flake8')}
                  className={`p-4 border rounded-lg flex flex-col items-center ${
                    linter === 'flake8' 
                    ? 'border-green-500 bg-green-50 text-green-700' 
                    : 'hover:bg-gray-50'
                  }`}
                >
                  <CheckCircle className="w-8 h-8 mb-2" />
                  <span className="font-semibold">Flake8</span>
                  <span className="text-sm text-gray-600 mt-1">PEP8 检查</span>
                </button>
              </div>
            </div>
          </div>
        );
        
      case 'deps':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">操作类型</label>
              <select
                value={depAction}
                onChange={(e) => setDepAction(e.target.value)}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
              >
                <option value="list">查看已安装包</option>
                <option value="install">安装包</option>
                <option value="update">更新包</option>
                <option value="remove">卸载包</option>
              </select>
            </div>
            
            {(depAction === 'install' || depAction === 'update' || depAction === 'remove') && (
              <div>
                <label className="block text-sm font-medium mb-2">包名称</label>
                <input
                  type="text"
                  value={packageName}
                  onChange={(e) => setPackageName(e.target.value)}
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                  placeholder="例如: numpy, pandas, requests"
                />
              </div>
            )}
            
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start">
                <Package className="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
                <div>
                  <h4 className="font-medium text-yellow-800">依赖管理说明</h4>
                  <p className="text-yellow-700 text-sm mt-1">
                    使用 pip 管理 Python 包依赖。支持安装、更新、卸载包，以及查看当前环境已安装的包列表。
                  </p>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'venv':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">操作类型</label>
              <select
                value={venvAction}
                onChange={(e) => setVenvAction(e.target.value)}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="list">查看虚拟环境</option>
                <option value="create">创建虚拟环境</option>
                <option value="activate">激活虚拟环境</option>
                <option value="delete">删除虚拟环境</option>
              </select>
            </div>
            
            {(venvAction === 'create' || venvAction === 'activate' || venvAction === 'delete') && (
              <div>
                <label className="block text-sm font-medium mb-2">虚拟环境名称</label>
                <input
                  type="text"
                  value={venvName}
                  onChange={(e) => setVenvName(e.target.value)}
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                  placeholder="例如: venv, myenv, project_env"
                />
              </div>
            )}
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <div className="flex items-start">
                <Cpu className="w-5 h-5 text-purple-600 mr-2 mt-0.5" />
                <div>
                  <h4 className="font-medium text-purple-800">虚拟环境说明</h4>
                  <p className="text-purple-700 text-sm mt-1">
                    虚拟环境可以隔离不同项目的依赖，避免包冲突。建议为每个Python项目创建独立的虚拟环境。
                  </p>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'run':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Python脚本路径</label>
              <div className="flex">
                <input
                  type="text"
                  value={scriptPath}
                  onChange={(e) => setScriptPath(e.target.value)}
                  className="flex-grow p-3 border rounded-l-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
                  placeholder="例如: ./scripts/main.py"
                />
                <button className="bg-gray-100 px-4 rounded-r-lg border border-l-0">
                  <FileCode className="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">脚本参数（可选）</label>
              <input
                type="text"
                value={scriptArgs}
                onChange={(e) => setScriptArgs(e.target.value)}
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
                placeholder="例如: --input data.csv --output result.json"
              />
            </div>
            
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-start">
                <Play className="w-5 h-5 text-red-600 mr-2 mt-0.5" />
                <div>
                  <h4 className="font-medium text-red-800">脚本执行说明</h4>
                  <p className="text-red-700 text-sm mt-1">
                    执行 Python 脚本文件。可以传递参数给脚本。确保脚本有可执行权限。
                  </p>
                </div>
              </div>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* 头部 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-xl">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">PyTools</h1>
                <p className="text-gray-600">Python 开发工具集 - 代码格式化、检查、依赖管理、虚拟环境管理</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                设置
              </button>
              <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                帮助
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 左侧面板 */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              {/* 标签页 */}
              <div className="border-b">
                <div className="flex overflow-x-auto">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex items-center space-x-2 px-6 py-4 whitespace-nowrap border-b-2 transition-colors ${
                          activeTab === tab.id
                            ? `${tab.color} border-current font-semibold`
                            : 'text-gray-500 border-transparent hover:text-gray-700'
                        }`}
                      >
                        <Icon className="w-5 h-5" />
                        <span>{tab.name}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* 内容区域 */}
              <div className="p-8">
                {renderContent()}
                
                {/* 执行按钮 */}
                <div className="mt-8 pt-6 border-t">
                  <button
                    onClick={handleExecute}
                    disabled={loading}
                    className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all ${
                      loading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
                    }`}
                  >
                    {loading ? (
                      <span className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        执行中...
                      </span>
                    ) : (
                      <span className="flex items-center justify-center">
                        <Play className="w-5 h-5 mr-2" />
                        执行命令
                      </span>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* 右侧输出面板 */}
          <div className="lg:col-span-1">
            <div className="bg-gray-900 rounded-2xl shadow-lg overflow-hidden h-full">
              <div className="bg-gray-800 px-6 py-4 border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Terminal className="w-5 h-5 text-green-400" />
                    <h2 className="text-lg font-semibold text-white">终端输出</h2>
                  </div>
                  <button 
                    onClick={() => setOutput('')}
                    className="px-3 py-1 text-sm bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors"
                  >
                    清空
                  </button>
                </div>
              </div>
              
              <div className="p-6 h-[calc(100%-80px)]">
                {output ? (
                  <div className="font-mono text-sm text-gray-300 whitespace-pre-wrap h-full overflow-y-auto">
                    {output}
                  </div>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center text-gray-500">
                    <Terminal className="w-16 h-16 mb-4" />
                    <p className="text-center">执行命令后，输出将显示在这里</p>
                    <p className="text-sm text-gray-600 mt-2">支持格式化和检查 Python 代码</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* 底部信息 */}
        <div className="mt-8 bg-white rounded-2xl shadow-lg p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">5</div>
              <div className="text-gray-600">核心功能</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">Python 3.7+</div>
              <div className="text-gray-600">支持版本</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">CLI + UI</div>
              <div className="text-gray-600">双模式</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;