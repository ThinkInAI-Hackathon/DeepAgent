# 1. 获取实例
```python
# 导入
>>> from wxautox import WeChat
# 获取微信窗口对象
>>> wx = WeChat()
初始化成功，获取到已登录窗口：xxxx
```
# 2. 发送消息相关
## 2.1 发送文字消息（打字机模式）
wx.SendTypingText
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| msg | str | / | 要发送的文字内容 |
| who | str | None| 要发送给谁，默认发送给当前打开的页面 |
| clear | bool | True | 是否清楚原本聊天框的内容 |
| at | list,str | None | 要@的人，可以是一个或多个人，格式为str或list，例如："张三"或["张三", "李四"] |
| exact | bool | False | who参数是否精确匹配，默认False |

返回值：无

示例：
```bash
# 发送消息
>>> who = '文件传输助手'
>>> msg = '''这是一条消息
这是第二行
这是第三行'''
wx.SendTypingText(msg, who=who)
# 换行及@功能
who = '工作群'
msg = '''各位下午好
{@张三}负责xxx
{@李四}负责xxxx'''
wx.SendTypingText(msg, who=who)
```

## 2.2 发送文件、图片、视频消息
wx.SendFiles
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| filepath | str,list | / | 指定文件路径，单个文件str，多个文件list |
| who | str | None | 要发送给谁，默认则发送给当前打开的页面 |
| exact | bool | False | who参数是否精确匹配，默认Flase |

返回值（bool）：如果发送成功则返回True，否则为False

示例：
```bash
# 给“文件传输助手”发送文件（图片同理）
>>> who = '文件传输助手'
# 指定文件路径（绝对路径）
>>> files = ['D:/test/test1.txt', 'D:/test/test2.txt', 'D:/test/test3.txt']
>>> wx.SendFiles(files, who=who)
```

# 3. 获取消息
## 3.1 获取历史消息
### 3.1.1 获取微信主窗口当前聊天窗口UI框架已加载所有聊天记录
wx.GetAllMessage
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| savepic | bool | False | 是否自动保存聊天图片 |
| savevideo | bool | False | 是否自动保存聊天视频 |
| savefile | bool | False | 是否自动保存聊天文件 |
| savevoice | bool | False | 是否自动保存语音转文字内容 |
| parseurl | bool | False | 是否自动获取卡片链接 |

返回值(List[Message])：返回一个消息列表，列表元素为 Message 对象。

### 3.1.2 加载微信主窗口当前聊天窗口UI框架更多消息
wx.LoadMoreMessage
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| interval | float | 0.3 | 滚动间隔时间，看自己电脑卡顿程度调整，默认0.3秒 |

返回值(bool)：成功加载返回True，否则返回False

## 3.3 监听模式获取消息（微信子窗口模式，无需消息免打扰，效率最高）
监听模式指的是将指定聊天窗口独立出去，是为了避免微信主窗口因为切换聊天页面导致目标窗口中聊天消息的UI元素消失，从而失去判断哪些是历史消息哪些是新消息的依据。这种方式对新消息判断的准确率高、获取效率也高，缺点是内存占用大、独立窗口有数量限制
### 3.3.1 添加监听对象
wx.AddListenChat
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| who | str | / | 要监听的群名或好友名 |
| savepic | bool | False | 是否自动保存聊天图片 |
| savevideo | bool | False | 是否自动保存聊天视频 |
| savefile | bool | False | 是否自动保存聊天文件 |
| savevoice | bool | False | 是否自动保存语音转文字内容 |
| parseurl | bool | False | 是否自动获取卡片链接 |
| exact | bool | False | who参数是否精确匹配，默认False |

### 3.3.2 获取监听消息
wx.GetListenMessage
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| who | str | None | 已监听的群名或好友名，不填则获取所有监听对象的新消息 |

返回值(Dict[ChatWnd, List[Message]])：返回一个字典，key为一个微信子窗口 ChatWnd 对象，详见 ChatWnd 对象相关说明；value为消息内容，list格式，列表元素为 Message 对象。

### 3.3.3 移除监听对象
wx.RemoveListenChat


返回值：无

# 4. 获取通讯录相关
## 4.1 获取通讯录好友
### 4.1.1 获取粗略信息
wx.GetAllFriends
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| keywords | str | None | 搜索并筛选关键词 |

示例：
```bash
>>> wx.GetAllFriends()
[{'nickname': '张三', 'remark': '张总', 'tags': None},
{'nickname': '李四', 'remark': None, 'tags': ['同事', '初中同学']},
{'nickname': '王五', 'remark': None, 'tags': None},
...]
```

### 4.1.2 获取详细信息
wx.GetFriendDetails
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| n | int | None | 获取前n个好友详情信息, 默认为None，获取所有好友详情信息 |
| tag | str | 'A' | 从哪个标签开始获取，A-Z其中一个 |
| timeout | int | 0xFFFFF  | 获取好友详情信息的超时时间，单位为秒 |

示例：
```bash
>>> wx.GetFriendDetails()
[{'微信号：': 'abc123456',
'地区：': '上海 浦东新区',
'备注': '',
'标签': 'wxauto',
'共同群聊': '1个',
'来源': '通过扫一扫添加',
'昵称': '张三'},
{'备注': '',
'企业': '广州融创文旅城',
'实名': '**莹',
'官方商城': '🎫购滑雪票入口🎫',
'通知': '回复时间为工作日9点-18点',
'会员商城': '🏂热雪值兑换雪票🏂',
'冰箱赞滑': '👬申请冰箱主理人👭',
'全民滑雪': '购票赢黄金会籍',
'共同群聊': '1个',
'昵称': '广州大冰箱'},...]
```

返回值(List[Dict[str, str]])：返回值是一个list，列表元素为dict，每个dict包含了一个好友的详细信息

# 5. 页面切换
## 5.1 切换微信主窗口聊天页面
wx.ChatWith
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| who | str | / | 要打开的聊天框好友名或群名 |
| exact | bool | False | who参数是否精确匹配，默认False |

返回值(str)：返回值为切换后的聊天名，一般等于who变量，在不精确匹配下可能不一样。
## 5.2 切换到通讯录页面
wx.SwitchToContact
## 5.3 切换到聊天页面
wx.SwitchToChat

# 6. 其他对象
## 6.1 消息对象 Message
消息对象指的是 GetAllMessage 、 GetListenMessage 等所有有关获取消息的方法返回的列表内的对象元素，一共有五种 Message 对象，分别是系统消息 SysMessage 、时间消息 TimeMessage 、撤回消息 RecallMessage 、自己发出的消息 SelfMessage 、朋友发来的消息 FriendMessage

所有消息对象都支持以下属性：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| type | str | 消息来源类型 |
| mtype | str | 消息内容类型，仅设置了保存某种类型的消息才会有，否则为空 |
| content | str | 消息内容 |
| sender | str | 发送者 |
| info | list | 原始消息信息，包含了消息的所有信息 |
| control | uiautomation.Control  | 该消息的uiautomation控件 |
| id | str | 消息id |
所有消息对象都支持以下方法：
- roll_into_view：将该消息滚动至聊天窗口可见位置，便于操作

### 6.1.1 系统消息 SysMessage
支持属性：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| type | str | 消息类型，固定为 sys |
| content | str | 消息内容 |
| sender | str | 发送者，固定为 SYS |
| info | list | 原始消息信息，包含了消息的所有信息 |
| control | uiautomation.Control  | 该消息的uiautomation控件 |
| id | str | 消息id |

### 6.1.2 时间消息 TimeMessage
支持属性：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| type | str | 消息类型，固定为 time |
| content | str | 消息内容 |
| sender | str | 发送者，固定为 Time |
| time | str | 时间消息内容，格式为 %Y-%m-%d %H:%M |
| info | list | 原始消息信息，包含了消息的所有信息 |
| control | uiautomation.Control  | 该消息的uiautomation控件 |
| id | str | 消息id |

### 6.1.3 自己发出的消息 SelfMessage
支持属性：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| type | str | 消息类型，固定为 self |
| mtype | str | 消息内容类型，text、image、video、file、voice、card |
| content | str | 消息内容 |
| sender | str | 发送者 |
| info | list | 原始消息信息，包含了消息的所有信息 |
| control | uiautomation.Control  | 该消息的uiautomation控件 |
| id | str | 消息id |

### 6.1.5 朋友发来的消息 FriendMessage
支持属性：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| type | str | 消息类型，固定为 friend |
| mtype | str | 消息内容类型，text、image、video、file、voice、card |
| content | str | 消息内容 |
| sender | str | 发送者 |
| sender_remark | str | 发送者备注名 |
| info | list | 原始消息信息，包含了消息的所有信息 |
| control | uiautomation.Control  | 该消息的uiautomation控件 |
| id | str | 消息id |

6.2 微信子窗口对象 ChatWnd

微信子窗口对象指的是从微信主窗口独立出来的聊天窗口，主要用于监听模式下对聊天窗口的各种操作。

支持属性：
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| who | str | 该子窗口对应的好友/群名 |
| UiaAPI | str | 该子窗口的uiautomation控件 |
| editbox | str | 该子窗口中消息编辑框的uiautomation控件 |
| savepic | bool | 用于设置监听模式时，是否自动下载图片 |
| savevideo | bool | 用于设置监听模式时，是否自动下载视频 |
| savefile | bool | 用于设置监听模式时，是否自动下载文件 |
| savevoice | bool | 用于设置监听模式时，是否自动获取语音转文字 |
| parseurl | bool | 用于设置监听模式时，是否自动解析卡片链接 |

我们将微信子窗口对象命名为chat，后续文档内不再重复定义：
```python
who = '张三'
savepic = True
savefile = False
savevoice = True
parseurl = False
wx.AddListenChat(
who
savepic=savepic,
savefile=savefile,
savevoice=savevoice,
parseurl=parseurl
) # 该方法会将“张三”的聊天窗口加入监听，并把他的聊天窗口独立出来，在wx.listen这个dict
中记录
wx.listen
# {'张三': <wxauto Chat Window at 0xbac39c32 for 张三>}
chat = wx.listen[who] # 后续文档内不再重复定义chat
```
### 6.2.1 加载该子窗口当前UI框架更多消息
chat.LoadMoreMessage
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| interval | float | 0.3 | 滚动间隔时间，看自己电脑卡顿程度调整，默认0.3秒 |
### 6.2.2 获该子窗口当前UI框架已加载所有聊天记录
chat.GetAllMessage
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| savepic | bool | False | 是否自动保存聊天图片 |
| savevideo | bool | False | 是否自动保存聊天视频 |
| savefile | bool | False | 是否自动保存聊天文件 |
| savevoice | bool | False | 是否自动保存语音转文字内容 |
| parseurl | bool | False | 是否自动获取卡片链接 |

8.2.3 发送文字消息（打字机模式）
chat.SendTypingText
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| msg | str | / | 要发送的文字内容 |
| clear | bool | True | 是否清楚原本聊天框的内容 |
| at | list,str | None | 要@的人，可以是一个或多个人，格式为str或list，例如："张三"或["张三", "李四"] |
| exact | bool | False | who参数是否精确匹配，默认False |
### 6.2.4 发送文件、图片、视频消息
chat.SendFiles
| 参数名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| filepath | str,list | / | 指定文件路径，单个文件str，多个文件list |