# 任务管理逻辑/处理任务操作
from datetime import datetime
from config import DATE_FORMAT

def add_task(tasks, description):
    """添加新任务"""
    new_task = {
        "desc": description,
        "completed": False,
        "created_at": datetime.now().strftime(DATE_FORMAT)
    }
    tasks.append(new_task)
    return tasks

def delete_task(tasks, index):
    """删除指定任务"""
    if 0 <= index < len(tasks):
        return tasks.pop(index)
    return None

def toggle_complete(tasks, index):
    """切换任务完成状态"""
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = not tasks[index]["completed"]
        tasks[index]["modified_at"] = datetime.now().strftime(DATE_FORMAT)
        return True
    return False