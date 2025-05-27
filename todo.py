# 导入模块（最顶部）
import os

# 常量定义（紧接导入）
FILE_NAME = "tasks.txt"

# 函数定义（核心位置）
def load_tasks():
    """从文件加载任务列表"""
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        return [{
            "desc": line.strip(),
            "completed": False # 默认状态为未完成
        } for line in f.readlines()]
    
def save_tasks(tasks):
    """保存任务列表到文件"""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        task_descriptions = [task["desc"] for task in tasks]
        f.write('\n'.join(task_descriptions))

# 主程序逻辑（底部）
if __name__ == "__main__": # Python项目标准写法，确保作为脚本直接运行时才执行主逻辑
    tasks = load_tasks() # 从文件初始化任务

    while True:
        print("\n待办事项清单")
        print("1. 添加任务")
        print("2. 删除任务")
        print("3. 查看任务")
        print("4. 标记任务完成")
        print("5. 退出")

        choice = input("请输入选项（1-5）：")

        # 添加任务
        if choice == '1':
            task = input("请输入新任务：")
            tasks.append(task)
            print(f"已添加任务：{task}")

        # 删除任务
        elif choice == '2':
            if not tasks:
                print("当前没有任务！")
                continue

            print("当前任务：")
            # 关键修正：遍历tasks而非task
            for index, task in enumerate(tasks, 1):
                status = "√" if task["completed"] else " "
                print(f"{index}. [{status}] {task['desc']}")

            try:
                task_num = int(input("请输入要删除的任务编号：")) - 1
                removed_task = tasks.pop(task_num)
                print(f"已删除：{removed_task}")
            except (ValueError, IndexError):
                print("无效的输入！")

        # 查看任务
        elif choice == '3':
            if not tasks:
                print("当前没有任务！")
            else:
                print("\n当前任务列表：")
                for index, task in enumerate(tasks, 1):
                    status = "√" if task["completed"] else " " # 根据状态显示勾选符号
                    print(f"{index}. [{status}] {task['desc']}")

        # 标记任务完成
        elif choice == '4':
            if not tasks:
                print("当前没有任务！")
                continue
            
            print("当前任务：")
            for index, task in enumerate(tasks, 1):
                status = "√" if task["completed"] else " "
                print(f"{index}. [{status}] {task['desc']}")

            try:
                task_num = int(input("请输入要标记的任务编号：")) - 1
                if 0 <= task_num < len(tasks): # 在删除和标记功能中添加更健壮的校验
                    # 切换完成状态（未完成↔已完成）
                    tasks[task_num]["completed"] = not tasks[task_num]["completed"]
                    print("状态已更新！")
                else:
                    print("编号超出范围！")
            except ValueError:
                print("请输入有效的数字编号！")

        # 退出
        elif choice == '5':
            save_tasks(tasks)
            print("数据已保存，再见！")
            break

        else:
            print("无效的选项，请重新输入")
