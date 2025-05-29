# 文件读写模块/处理文件储存
import json
import os 
from datetime import datetime
from config import TASK_FILE, DATA_DIR, DATE_FORMAT, DATA_VERSION

# ================= 数据迁移函数 =================
def migrate_v1_to_v2(data):
    """v1 (纯文本列表) → v2 (基础JSON格式)"""
    return {
        "version": 2,
        "tasks": [
            {"desc": desc, "completed": False}
            for desc in data
        ]
    }

def migrate_v2_to_v3(data):
    """v2 → v3 (添加时间戳字段)"""
    now = datetime.now().strftime(DATE_FORMAT)
    for task in data["tasks"]:
        task.setdefault("created_at", now)
        task.setdefault("modified_at", now)
    data["version"] = 3
    return data

# ================= 迁移注册表 =================
MIGRATIONS = {
    1: migrate_v1_to_v2,
    2: migrate_v2_to_v3
}

# ================= 核心功能 =================
def load_tasks():
    """加载任务数据并自动执行版本迁移"""
    # 创建数据目录（如果不存在）
    os.makedirs(DATA_DIR, exist_ok=True)

    # 处理文件不存在的情况
    if not os.path.exists(TASK_FILE):
        return {"version": DATA_VERSION, "tasks": []}
    
    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            # 处理空文件情况
            content = f.read().strip()
            if not content:
                return {"version": DATA_VERSION, "tasks": []}
            
            data = json.loads(content)

            # 旧数据格式处理
            if isinstance(data, list):
                data = {"version": 1, "tasks": data}

            # 执行增量迁移
            while data["version"] < DATA_VERSION:
                migration_func = MIGRATIONS.get(data["version"])
                if not migration_func:
                    raise ValueError(f"找不到版本 {data['version']}的迁移方案")
                data = migration_func(data)
            
            return data
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"数据加载失败: {str(e)}")
        return {"version": DATA_VERSION, "tasks": []}
    
def save_tasks(data):
    """保存任务数据（需包含完整版本信息）"""
    if "version" not in data or "tasks" not in data:
        raise ValueError("数据格式必须包含 version 和 tasks 字段")
    
    # 确保使用最新版本格式
    data["version"] = DATA_VERSION

    # 更新修改时间戳
    for task in data["tasks"]:
        task["modified_at"] = datetime.now().strftime(DATE_FORMAT)
    
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump(
            data, f,
            ensure_ascii=False,     # 允许保存中文
            indent=2,               # 美化格式
            default=str             # 处理datetime对象的序列化
        )