from typing import Protocol, List, Dict, TypedDict
from datetime import datetime

# 定义任务数据结构
class TaskData(TypedDict):
    desc: str
    completed: bool
    created_at: datetime
    modified_at: datetime

# 任务管理接口
class ITaskManager(Protocol):
    def add_task(self, tasks: List[TaskData], description: str) -> List[TaskData]: ...

    def delete_task(self, tasks: List[TaskData], index: int) -> tuple[List[TaskData], TaskData]: ...

    def toggle_complete(self, tasks: List[TaskData], index: int) -> bool: ...

# 数据管理接口
class IDataManager(Protocol):
    def load(self) -> List[TaskData]: ...

    def save(self, tasks: List[TaskData]) -> None: ...

# 用户界面接口
class IUserInterface(Protocol):
    def run(self) -> None: ...