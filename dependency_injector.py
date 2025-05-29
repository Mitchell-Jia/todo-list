from interfaces import IUserInterface, IDataManager, ITaskManager
from data_manager import DataManager
from task_manager import TaskManager
from gui import TodoGUI
from cli import TodoCLI
from config import TASK_FILE

class AppFactory:
    """应用组件工厂"""

    @staticmethod
    def create_data_manager() -> IDataManager:
        return DataManager()
    
    @staticmethod
    def create_task_manager() -> ITaskManager:
        return TaskManager()
    
    @staticmethod
    def create_gui_interface(
        task_manager: ITaskManager,
        data_manager: IDataManager
    ) -> IUserInterface:
        return TodoGUI(task_manager, data_manager)
    
    @staticmethod
    def create_cli_interface(
        task_manager: ITaskManager,
        data_manager: IDataManager
    ) -> IUserInterface:
        return TodoCLI(task_manager, data_manager)