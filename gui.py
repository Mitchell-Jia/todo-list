# gui模式
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List

from interfaces import IUserInterface, ITaskManager, IDataManager

class TodoGUI(IUserInterface):
    def __init__(self, 
                 task_manager: ITaskManager,
                 data_manager: IDataManager):
        self.task_manager = task_manager
        self.data_manager = data_manager
        self.tasks: List[dict] = []
        self.root = tk.Tk()
        self.root.title("待办事项管理器")
        self.root.geometry("800x600")

    def run(self):
        self._load_data()       # 加载数据
        self._create_ui()       # 创建ui
        self.root.mainloop()
        
    def _load_data(self):
        self.tasks = self.data_manager.load()

    def _create_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 任务列表
        self.listbox = tk.Listbox(
            main_frame,
            width=60,
            height=15,
            font=("微软雅黑", 11)
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 刷新列表
        self._refresh_list()

        # 按钮框架
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="添加任务", command=self._add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除任务", command=self._delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="标记完成", command=self._toggle_complete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="刷新列表", command=self._refresh_list).pack(side=tk.RIGHT, padx=5)
    
    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "√" if task.get("completed", False) else "  "
            self.listbox.insert(tk.END, f"[{status}] {task['desc']}")

    def _add_task(self):
        # 弹出输入对话框
        desc = simpledialog.askstring(
            "添加新任务", 
            "请输入任务描述:",
            parent=self.root
        )
        
        # 用户点击取消或关闭对话框
        if desc is None:
            return
            
        # 去除首尾空格
        desc = desc.strip()
        
        # 验证输入
        if not desc:
            messagebox.showerror("错误", "任务描述不能为空！")
            return
            
        try:
            # 添加任务
            self.tasks = self.task_manager.add_task(self.tasks, desc)
            self.data_manager.save(self.tasks)
            self._refresh_list()
            messagebox.showinfo("成功", f"已添加任务: {desc}")
        except ValueError as e:
            messagebox.showerror("错误", str(e))     
    
    def _delete_task(self):
        try:
            selection = self.listbox.curselection()
            if selection:
                index = selection[0]
                self.tasks, deleted = self.task_manager.delete_task(self.tasks, index)
                self.data_manager.save(self.tasks)
                self._refresh_list()
                messagebox.showinfo("删除成功", f"已删除任务: {deleted['desc']}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _toggle_complete(self):
        try:
            selection = self.listbox.curselection()
            if selection:
                index = selection[0]
                if self.task_manager.toggle_complete(self.tasks, index):
                    self.data_manager.save(self.tasks)
                    self._refresh_list()
                    status = "完成" if self.tasks[index]["completed"] else "未完成"
                    messagebox.showinfo("状态更新", f"任务已标记为: {status}")
        except Exception as e:
            messagebox.showerror("错误", str(e))