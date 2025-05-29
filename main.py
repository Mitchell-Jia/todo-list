import sys

from dependency_injector import AppFactory
from interfaces import IUserInterface

def create_app(mode: str) -> IUserInterface:
    # 创建核心服务
    data_manager = AppFactory.create_data_manager()
    task_manager = AppFactory.create_task_manager()

    #创建ui
    if mode == "gui":
        return AppFactory.create_gui_interface(task_manager, data_manager)
    return AppFactory.create_cli_interface(task_manager, data_manager)
    
if __name__ == "__main__":
    mode = "cli" if "--cli" in sys.argv else "gui"

    try:
        app = create_app(mode)
        print(f"启动 {mode.upper()} 模式...")
        app.run()
    except Exception as e:
        print(f"应用启动失败: {str(e)}")
        sys.exit(1)