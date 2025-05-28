# cli模式
import sys
from datetime import datetime
from config import DATE_FORMAT, DATA_VERSION
from file_handler import load_tasks, save_tasks
from task_manager import add_task, delete_task, toggle_complete

def show_menu():
    """显示主菜单"""
    print("\n待办事项清单")
    print("1. 添加任务")
    print("2. 删除任务")
    print("3. 查看任务")
    print("4. 标记任务")
    print("5. 退出程序")

def display_tasks(tasks):
    """"显示任务列表"""
    if not tasks:
        print("\n当前没有任务!")
        return
    
    print("\n任务列表:")
    for index, task in enumerate(tasks, 1):
        status = "√" if task["completed"] else " "
        created = datetime.strptime(task["created_at"], DATE_FORMAT).strftime("%m/%d %H:%M")
        desc = f"[{status}] {task['desc']} (创建于: {created})"
        print(f"{index}. {desc}")

def get_valid_index(prompt, max_index):
    """获取有效任务索引"""
    while True:
        try:
            index = int(input(prompt)) - 1
            if 0 <= index < max_index:
                return index
            print(f"请输入 1 到 {max_index} 之间的数字")
        except ValueError:
            print("请输入有效数字！")

def start_cli():
    data = load_tasks()
    tasks = data["tasks"] if isinstance(data, dict) else data

    while True:
        show_menu()
        choice = input("请输入选项(1-5):").strip()

        if choice == '1':
            # 添加任务逻辑
            desc = input("请输入新任务：").strip()
            if desc:
                tasks = add_task(tasks, desc)
                save_tasks({
                    "version": DATA_VERSION,
                    "tasks": tasks
                })
                print(f"已添加任务：{desc}")
            else:
                print("错误:任务描述不能为空！")

        elif choice == '2':
            # 删除任务逻辑
            if not tasks:
                print("当前没有可删除的任务！")
                continue
            display_tasks(tasks)

            index = get_valid_index("请输入要删除的任务编号：", len(tasks))
            new_tasks, deleted = delete_task(tasks, index)
            if deleted:
                save_tasks({
                    "version": DATA_VERSION,
                    "tasks": new_tasks
                })
                tasks = new_tasks
                print(f"已删除任务: {deleted['desc']}")

        elif choice == '3':
            display_tasks(tasks)
        
        elif choice == '4':
            # 标记完成逻辑
            if not tasks:
                print("当前没有可标记的任务！")
                continue
            display_tasks(tasks)

            index = get_valid_index("输入要标记的任务编号: ", len(tasks))
            if toggle_complete(tasks, index):
                save_tasks({
                    "version": DATA_VERSION,
                    "tasks": tasks
                })
                status = "完成" if tasks[index]["completed"] else "未完成"
                print(f"任务已标记为: {status}")

        elif choice == '5':
            save_tasks({
                    "version": DATA_VERSION,
                    "tasks": tasks
                })
            print("数据已保存，再见！")
            sys.exit()

        else:
            print("无效选项，请重新输入!")

if __name__ == "__main__":
    start_cli()