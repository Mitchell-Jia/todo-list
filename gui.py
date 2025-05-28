# gui模式
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import DATE_FORMAT, DATA_VERSION
from file_handler import load_tasks, save_tasks
from task_manager import add_task, delete_task, toggle_complete

class TodoApp: # 类
    def __init__(self, root):
        self.root = root
        self.root.title("待办事项管理器")
        self.root.geometry("800x600")

        # 加载数据
        self._load_data()
        
        # 配置样式
        self._configure_styles()
        
        # 创建界面组件
        self._create_widgets()

        # 初始化状态栏
        self._create_status_bar()
    
    def _load_data(self):
        """加载任务数据"""
        data = load_tasks()
        # 确保数据结构正确
        self.tasks = data.get("tasks", []) if isinstance(data, dict) else data


    def _configure_styles(self):
        """配置全局样式"""
        style = ttk.Style()

        # 主界面样式
        style.configure("TButton", 
            padding=6, 
            font=("微软雅黑", 10),
            foreground="#2c3e50"
        )
        
        # 输入框样式
        style.configure("TEntry",
            font=('微软雅黑', 10)
        )

        # 列表样式
        style.configure("TListbox", 
            font=("Consolas", 11),
            background="#ffffff",
            selectbackground="#3498db"
        )
        
        # 状态栏样式
        style.configure("Status.TLabel",
            background="#bdc3c7",
            font=("微软雅黑", 9),
            padding=(5, 2)
        )

    def _create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # 任务列表
        self.listbox = tk.Listbox(
            main_frame,
            width=60,
            height=15,
            font=("微软雅黑", 11),
            selectmode=tk.SINGLE
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 刷新列表
        self.refresh_list()

        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, 
            text="➕ 添加任务",
            command=self.add_task
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame,
            text="🗑️ 删除任务",
            command=self.delete_task
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame,
            text="✅ 标记完成",
            command=self.toggle_complete
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame,
            text="🔄 刷新列表",
            command=self.refresh_list
        ).pack(side=tk.RIGHT, padx=5)

    def _create_status_bar(self):
        """创建状态栏组件"""
        self.status_text = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_text,
            anchor=tk.W,
            style="Status.TLabel"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("就绪")  # 初始化状态

    def update_status(self, message):
        """更新状态栏信息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.set(f"[{timestamp}] {message}")

    def refresh_list(self):
        """刷新任务列表显示"""
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task.get("completed", False) else "  "
            desc = task["desc"]
            created = datetime.strptime(
                task["created_at"], 
                DATE_FORMAT
            ).strftime("%m/%d %H:%M")
            self.listbox.insert(tk.END, 
                f"[{status}] {desc} (创建于: {created})"
            )
        
    def add_task(self):
        """添加新任务弹窗"""
        # 创建弹出窗口
        popup = tk.Toplevel(self.root)                  # 创建独立于主窗口的弹窗
        popup.title("添加新任务")
        popup.geometry("400x200")

        # 设置居中显示
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"+{x}+{y}")

        # 输入框组件
        ttk.Label(popup, text="任务描述:").pack(pady=5)
        entry_desc = ttk.Entry(popup, width=30)
        entry_desc.pack(pady=5)
        entry_desc.focus_set()                              # 自动聚焦输入框提升用户体验

        # 保存按钮逻辑
        def save_task():
            desc = entry_desc.get().strip()                 # strip()去除输入内容的首尾空格
            if not desc:
                messagebox.showwarning("警告","任务描述不能为空！")  # 输入验证：防止添加空任务
                return
            try:
                self.tasks = add_task(self.tasks, desc)     # 调用 taks_manager 模块的添加功能
                save_tasks({  # 修正保存调用
                    "version": DATA_VERSION,
                    "tasks": self.tasks
                })                                          # 保存数据
                self.refresh_list()                         # 刷新列表
                self.update_status(f"已添加任务: {desc}")
                popup.destroy()                             # 关闭弹窗
            except Exception as e:
                messagebox.showerror("保存失败", f"发生错误: {str(e)}")
            # 更新状态栏
            self.status.config(text=f"已添加任务：{desc}")      # 在状态栏显示反馈操作

        # 保存按钮
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="保存", command=save_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=popup.destroy).pack(side=tk.LEFT, padx=5)

    def delete_task(self):
        """删除选中任务"""
        try:
            index = self.listbox.curselection()[0]
            new_tasks, _delete_task = delete_task(self.tasks, index)

            if _delete_task is not None:
                self.tasks = new_tasks
                save_tasks({
                    "version": DATA_VERSION,
                    "tasks": self.tasks
                })
                self.refresh_list()
                self.status_text.set(f"已删除任务: {_delete_task['desc']}")
            else:
                self.status_text.set("删除失败:无效索引")
            
        except IndexError:
            messagebox.showwarning("操作错误", "请先选中一个任务！")
        except Exception as e:
            messagebox.showerror("操作失败", f"删除时发生错误: {str(e)}")
    
    def toggle_complete(self):
        """切换完成状态"""
        try:
            index = self.listbox.curselection()[0]
            if toggle_complete(self.tasks, index):
                save_tasks({
                    "version":DATA_VERSION,
                    "tasks": self.tasks
                })
                self.refresh_list()
                status = "完成" if self.tasks[index]["completed"] else "未完成"
                self.update_status(f"任务状态已更新为: {status}")
            else:
                self.update_status("标记失败：无效的任务索引")
                
        except IndexError:
            messagebox.showwarning("操作错误", "请先选中一个任务！")
        except Exception as e:
            messagebox.showerror("操作失败", f"状态更新失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()