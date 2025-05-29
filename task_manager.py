# 任务管理逻辑/处理任务操作
from datetime import datetime

from interfaces import TaskData, ITaskManager
from config import DATE_FORMAT

class TaskManager(ITaskManager):
    def add_task(self, tasks: list[TaskData], description: str) -> list[TaskData]:
        if not description.strip():
            raise ValueError("任务描述不能为空")
        
        now = datetime.now().strftime(DATE_FORMAT)
        new_task: TaskData = {
            "desc": description.strip(),
            "completed": False,
            "created_at": now,
            "modified_at": now
        }
        return [*tasks, new_task]

    def delete_task(self, tasks: list[TaskData], index: int) -> tuple[list[TaskData], TaskData]:
        if not 0 <= index < len(tasks):
            raise ValueError(f"无效索引: {index}")
        return [t for i, t in enumerate(tasks) if i != index], tasks[index]

    def toggle_complete(self, tasks: list[TaskData], index: int) -> bool:
        if not 0 <= index < len(tasks):
            raise False
        tasks[index]["completed"] = not tasks[index]["completed"]
        tasks[index]["modified_at"] = datetime.now().strftime(DATE_FORMAT)
        return True