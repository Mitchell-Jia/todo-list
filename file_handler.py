# 文件读写模块/处理文件储存
import json
import os 
from datetime import datetime
from config import TASK_FILE, DATA_DIR

def load_tasks():
    """加载任务数据"""
    # 创建数据目录（如果不存在）
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            # 兼容旧版本文本格式
            if tasks and isinstance(tasks[0], str): # 检测旧版文本格式
                return migrate_legacy(tasks)
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_tasks(tasks):
    """保存任务数据"""
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f,
                  ensure_ascii=False,   # 允许保存中文
                  indent=2,            # 美化格式
                  default=str)          # 处理datetime对象的序列化

def migrate_legacy(old_tasks):
    """迁移旧版文本数据"""
    print("检测到旧版数据格式，正在自动迁移...")
    return [{"desc": task, "completed": False} for task in old_tasks]