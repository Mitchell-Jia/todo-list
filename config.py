# 存储配置项/配置常量
import os

# 数据版本配置
DATA_VERSION = 3  # 当前数据版本

# 文件路径配置
DATA_DIR = "data"  # 数据存储目录
TASK_FILE = os.path.join(DATA_DIR, "tasks.json")  # 数据文件路径

# 时间格式配置
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # ISO 8601扩展格式

"""
版本历史：
v1 - 纯文本格式         (每行一个任务描述)
v2 - 初始JSON格式       (包含desc/completed)
v3 - 添加时间戳字段     (created_at/modified_at)
"""