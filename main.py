# 主程序/负责界面和流程
import sys
from file_handler import load_tasks, save_tasks
from task_manager import add_task, delete_task, toggle_complete

def show_menu():
    """显示主菜单"""
    print("\n待办事项清单")
    print("1. 添加任务")
    print("2. 删除任务")
    print("3. 查看任务")
    print("4. 标记任务")
    print("5. 退出")

def display_tasks(tasks):
    """"显示任务列表"""
    if not tasks:
        print("当前没有任务！")
        return
    
    print("\n任务列表:")
    for index, task in enumerate(tasks, 1):
        status = "√" if task["completed"] else " "
        desc = task["desc"]
        print(f"{index}. [{status}] {desc}")

def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("请输入选项(1-5):")

        if choice == '1':
            # 添加任务逻辑
            desc = input("请输入新任务：")
            tasks = add_task(tasks, desc)
            print(f"已添加任务：{desc}")

        elif choice == '2':
            # 删除任务逻辑
            display_tasks(tasks)
            try:
                index = int(input("请输入要删除的任务编号：")) - 1
                if delete_task(tasks, index):
                    print("删除成功!")
            except ValueError:
                print("请输入有效数字！")

        elif choice == '3':
            display_tasks(tasks)
        
        elif choice == '4':
            # 标记完成逻辑
            display_tasks(tasks)
            try:
                index = int(input("请输入要标记的任务编号：")) - 1
                if  toggle_complete(tasks, index):
                    print("状态已更新！")
                else:
                    print("无效编号！")
            except ValueError:
                print("请输入有效数字！")

        elif choice == '5':
            save_tasks(tasks)
            print("数据已保存，再见！")
            sys.exit()

        else:
            print("无效选项，请重新输入!")

if __name__ == "__main__":
    main()
