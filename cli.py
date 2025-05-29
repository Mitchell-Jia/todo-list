# cli模式
from datetime import datetime
from typing import List

from config import DATE_FORMAT
from interfaces import IUserInterface, ITaskManager, IDataManager

class TodoCLI(IUserInterface):
    def __init__(self,
                 task_manager: ITaskManager,
                 data_manager: IDataManager):
        self.task_manager = task_manager
        self.data_manager = data_manager
        self.tasks: List[dict] = []

    def run(self):
        self.tasks = self.data_manager.load()
        while True:
            self._show_menu()
            choice = input("请选择选项(1-5):").strip()
            
            if choice == "1":
                self._add_task()
            elif choice == '2':
                self._delete_task()
            elif choice == '3':
                self._list_tasks()
            elif choice == '4':
                self._toggle_complete()
            elif choice == '5':
                self.data_manager.save(self.tasks)
                print("数据已保存，再见！")
                break
            else:
                print("无效选项，请重新输入!")
    
    def _show_menu(self):
        print("\n待办事项清单")
        print("1. 添加任务")
        print("2. 删除任务")
        print("3. 查看任务")
        print("4. 标记任务")
        print("5. 退出程序")

    def _add_task(self):
        desc = input("输入任务描述:").strip()
        if desc:
            try:
                self.tasks = self.task_manager.add_task(self.tasks, desc)
                self.data_manager.save(self.tasks)
                print(f"已添加任务: {desc}")
            except ValueError as e:
                print(f"错误: {str(e)}")
        else:
            print("错误:任务描述不能为空！")

    def _delete_task(self):
        if not self.tasks:
            print("当前没有可删除的任务！")
            return
        
        self._list_tasks()
        try:
            index = int(input("请输入要删除的任务编号:")) - 1
            if 0 <= index < len(self.tasks):
                self.tasks, deleted = self.task_manager.delete_task(self.tasks, index)
                self.data_manager.save(self.tasks)
                print(f"已删除任务: {deleted['desc']}")
            else:
                print("无效的任务编号")
        except ValueError:
            print("请输入有效数字！")

    def _list_tasks(self):
        if not self.tasks:
            print("\n当前没有任务!")
            return
        
        print("\n任务列表:")
        for i, task in enumerate(self.tasks, 1):
            status = "√" if task["completed"] else " "
            print(f"{i}. [{status}] {task['desc']}")

    def _toggle_complete(self):
        if not self.tasks:
            print("当前没有可标记的任务！")
            return
        
        self._list_tasks()
        try:
            index = int(input("请输入要标记的任务编号:")) - 1
            if 0 <= index < len(self.tasks):
                if self.task_manager.toggle_complete(self.tasks, index):
                    self.data_manager.save(self.tasks)
                    status = "完成" if self.tasks[index]["completed"] else "未完成"
                    print(f"任务已标记为: {status}")
                else:
                    print("标记失败")
            else:
                print("无效的任务编号")
        except ValueError:
            print("请输入有效数字！")