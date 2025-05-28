# 任务管理逻辑/处理任务操作
from datetime import datetime
from config import DATE_FORMAT

def add_task(tasks, description):
    """添加新任务（返回新列表）"""
    if not description.strip():
        raise ValueError("任务描述不能为空")
    
    now = datetime.now().strftime(DATE_FORMAT)
    return tasks + [{
        "desc": description.strip(),
        "completed": False,
        "created_at": now,
        "modified_at": now
    }]

def delete_task(tasks, index):
    """安全删除任务（返回新列表和被删任务）"""
    if 0 <= index < len(tasks):
        return [t for i, t in enumerate(tasks) if i != index], tasks[index]
    return tasks, None

def toggle_complete(tasks, index):
    """切换任务完成状态"""
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = not tasks[index]["completed"]
        tasks[index]["modified_at"] = datetime.now().strftime(DATE_FORMAT)  # 显示更新
        return True
    return False