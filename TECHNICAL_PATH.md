# 微信机器人技术路径

## 1. 技术栈

### 1.1 核心组件
- **FastMCP**: 用于构建 MCP (Model Context Protocol) 服务器，提供标准化的工具和资源接口
- **wxautox**: 微信自动化操作库，提供与微信客户端的交互能力
- **Python 3.11+**: 主要开发语言
- **Uvicorn**: ASGI 服务器，用于运行 FastMCP 服务

### 1.2 通信协议
- **SSE (Server-Sent Events)**: 用于服务器和客户端之间的实时通信
- **HTTP/HTTPS**: 基础通信协议

## 2. 系统架构

### 2.1 整体架构
```
[客户端] <---> [FastMCP Server] <---> [wxautox] <---> [微信客户端]
```

### 2.2 核心模块
1. **FastMCP 服务器层**
   - 提供标准化的 API 接口
   - 处理客户端请求
   - 管理工具和资源的生命周期

2. **微信操作层 (wxautox)**
   - 处理微信窗口操作
   - 管理消息收发
   - 处理文件传输
   - 管理聊天历史

3. **工具层**
   - 消息发送工具
   - 文件传输工具
   - 好友管理工具
   - 聊天历史工具

## 3. 功能实现

### 3.1 消息处理
- **发送文本消息**
  ```python
  @mcp.tool()
  async def send_text(msg: str, who: str, ...)
  ```
  - 自动切换到目标聊天
  - 支持打字机模式发送
  - 支持清除输入框

- **发送文件**
  ```python
  @mcp.tool()
  async def send_files(filepath: Union[str, List[str]], who: str, ...)
  ```
  - 支持单个/多个文件发送
  - 自动切换到目标聊天
  - 支持图片、视频等多媒体文件

### 3.2 聊天历史
- **获取历史消息**
  ```python
  @mcp.tool()
  async def get_history_messages(who: str, min_messages: int = 10, ...)
  ```
  - 支持自动加载更多消息
  - 支持保存图片/视频/文件
  - 支持语音转文字
  - 支持解析链接卡片

### 3.3 好友管理
- **获取好友列表**
  ```python
  @mcp.tool()
  async def get_friends(tags: Optional[List[str]] = None, ...)
  ```
  - 支持按标签筛选
  - 获取好友详细信息
  - 支持备注名和标签管理

## 4. 安全考虑

### 4.1 访问控制
- 服务器运行在本地
- 使用 SSE 协议确保实时性
- 支持精确匹配聊天对象

### 4.2 错误处理
- 完整的异常捕获和处理
- 详细的日志记录
- 操作状态反馈

## 5. 部署方案

### 5.1 环境要求
- Python 3.11+
- 已登录的微信客户端
- 必要的 Python 包依赖

### 5.2 启动流程
1. 初始化 FastMCP 服务器
2. 配置微信实例
3. 注册工具和资源
4. 启动 SSE 服务

## 6. 扩展性

### 6.1 可扩展点
- 支持添加新的工具函数
- 支持自定义资源类型
- 支持更多的微信操作功能

### 6.2 未来规划
- 支持群管理功能
- 添加消息过滤功能
- 支持更多的自动化操作
- 添加定时任务支持

## 7. 使用示例

### 7.1 发送消息
```python
# 发送文本消息
await client.call_tool("send_text", {
    "msg": "Hello, World!",
    "who": "文件传输助手",
    "exact": True
})

# 发送文件
await client.call_tool("send_files", {
    "filepath": ["path/to/file1.txt", "path/to/file2.jpg"],
    "who": "文件传输助手",
    "exact": True
})
```

### 7.2 获取历史消息
```python
# 获取聊天历史
await client.call_tool("get_history_messages", {
    "who": "文件传输助手",
    "min_messages": 20,
    "savepic": True,
    "savevoice": True
})
```

## 8. 注意事项

### 8.1 使用限制
- 需要保持微信客户端登录状态
- 避免频繁切换聊天窗口
- 注意文件路径的正确性

### 8.2 最佳实践
- 使用精确匹配避免发送错误
- 合理设置消息加载数量
- 及时处理异常情况
- 保持日志记录 