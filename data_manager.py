import logging
from typing import List

from config import DATA_VERSION
from interfaces import IDataManager, TaskData
from file_handler import load_tasks, save_tasks

class DataManager(IDataManager):
    def __init__(self):
        self.logger = logging.getLogger("DataManager")

    def load(self) -> List[TaskData]:
        try:
            data = load_tasks()
            if isinstance(data, dict) and "tasks" in data:
                return data["tasks"]
        except Exception as e:
            logging.error(f"数据加载失败: {str(e)}")
            return []
    
    def save(self, tasks: List[TaskData]) -> None:
        try:
            data = {
                "version": DATA_VERSION,
                "tasks": tasks
            }
            save_tasks(data)
        except Exception as e:
            self.logger.error(f"数据保存失败: {str(e)}")
            raise