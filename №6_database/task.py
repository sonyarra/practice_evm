import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("1000x600")
        
        self.setup_styles()
        
        self.connection = None
        self.connect_to_database()
        
        if self.connection:
            self.get_table_structure()
            
            self.create_widgets()
            
            self.load_users()
            self.load_categories()
            self.load_tasks()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.colors = {
            'bg': '#f0f0f0',
            'header': '#2c3e50',
            'success': '#27ae60',
            'warning': '#e67e22',
            'danger': '#e74c3c',
            'info': '#3498db'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host='mysql-ru-r1.joinserver.xyz',
                port=3306,
                database='s482226_NKEiVT2',
                user='u482226_LZzukV3PM4',
                password='KJV6k90B4r98QTwx+a=cG^@Y'
            )
            
            if self.connection.is_connected():
                print("Успешно подключено к базе данных")
                db_info = self.connection.get_server_info()
                print(f"Версия MySQL: {db_info}")
                
        except Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            messagebox.showerror("Ошибка", f"Не удалось подключиться к БД:\n{e}")
            self.connection = None
    
    def get_table_structure(self):
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\n📊 Существующие таблицы в базе данных:")
            for table in tables:
                print(f"  - {table[0]}")
            
            self.table_columns = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                self.table_columns[table_name] = [col[0] for col in columns]
                print(f"\nСтруктура таблицы '{table_name}':")
                for col in columns:
                    print(f"  {col[0]} - {col[1]}")
            
            cursor.close()
            
        except Error as e:
            print(f"Ошибка получения структуры таблиц: {e}")
            self.table_columns = {}
    
    def create_widgets(self):
        
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=50)
        header_frame.pack(fill='x')
        
        title_label = tk.Label(header_frame, text="Менеджер задач", 
                              font=('Arial', 16, 'bold'), 
                              fg='white', bg=self.colors['header'])
        title_label.pack(side='left', padx=20, pady=10)
        
        status_text = "Подключено к БД" if self.connection else "Нет подключения"
        status_color = 'green' if self.connection else 'red'
        self.status_label = tk.Label(header_frame, text=status_text, 
                                   fg=status_color, bg=self.colors['header'])
        self.status_label.pack(side='right', padx=20, pady=10)
        
        if not self.connection:
            return
        
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(main_container, bg='white', relief='groove', bd=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        tasks_header = tk.Frame(left_frame, bg=self.colors['info'], height=30)
        tasks_header.pack(fill='x')
        tk.Label(tasks_header, text="Список задач", font=('Arial', 10, 'bold'),
               fg='white', bg=self.colors['info']).pack(side='left', padx=10, pady=5)
        
        self.tasks_tree = ttk.Treeview(left_frame, 
                                       columns=('ID', 'Название', 'Статус', 'Приоритет', 'Срок', 'Категория'),
                                       show='headings',
                                       height=20)
        
        self.tasks_tree.heading('ID', text='ID')
        self.tasks_tree.heading('Название', text='Название')
        self.tasks_tree.heading('Статус', text='Статус')
        self.tasks_tree.heading('Приоритет', text='Приоритет')
        self.tasks_tree.heading('Срок', text='Срок')
        self.tasks_tree.heading('Категория', text='Категория')
        
        self.tasks_tree.column('ID', width=50)
        self.tasks_tree.column('Название', width=200)
        self.tasks_tree.column('Статус', width=100)
        self.tasks_tree.column('Приоритет', width=100)
        self.tasks_tree.column('Срок', width=100)
        self.tasks_tree.column('Категория', width=100)
        
        scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        self.tasks_tree.bind('<<TreeviewSelect>>', self.on_task_select)
        
        right_frame = tk.Frame(main_container, bg='white', relief='groove', bd=1, width=300)
        right_frame.pack(side='right', fill='y', padx=(5, 0))
        right_frame.pack_propagate(False)
        
        form_frame = tk.Frame(right_frame, bg='white')
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Название задачи:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
        self.title_entry = tk.Entry(form_frame, font=('Arial', 10))
        self.title_entry.pack(fill='x', pady=(0,5))
        
        tk.Label(form_frame, text="Описание:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
        self.desc_text = tk.Text(form_frame, height=4, font=('Arial', 10))
        self.desc_text.pack(fill='x', pady=(0,5))
        
        tk.Label(form_frame, text="Статус:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
        self.status_var = tk.StringVar(value='новая')
        status_frame = tk.Frame(form_frame, bg='white')
        status_frame.pack(fill='x', pady=(0,5))
        
        statuses = ['новая', 'в работе', 'завершена', 'отложена']
        for status in statuses:
            tk.Radiobutton(status_frame, text=status, variable=self.status_var, 
                         value=status, bg='white').pack(side='left', padx=5)
        
        tk.Label(form_frame, text="Приоритет:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
        self.priority_var = tk.StringVar(value='средний')
        priority_frame = tk.Frame(form_frame, bg='white')
        priority_frame.pack(fill='x', pady=(0,5))
        
        priorities = ['низкий', 'средний', 'высокий']
        for priority in priorities:
            tk.Radiobutton(priority_frame, text=priority, variable=self.priority_var,
                         value=priority, bg='white').pack(side='left', padx=5)
        
        tk.Label(form_frame, text="Срок выполнения (ГГГГ-ММ-ДД):", bg='white', anchor='w').pack(fill='x', pady=(5,0))
        self.due_entry = tk.Entry(form_frame, font=('Arial', 10))
        self.due_entry.pack(fill='x', pady=(0,5))
        self.due_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(form_frame, text="Пользователь:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
        self.user_combo = ttk.Combobox(form_frame, state='readonly')
        self.user_combo.pack(fill='x', pady=(0,5))
        
        tk.Label(form_frame, text="Категория:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
        self.category_combo = ttk.Combobox(form_frame, state='readonly')
        self.category_combo.pack(fill='x', pady=(0,5))
        
        buttons_frame = tk.Frame(right_frame, bg='white')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        self.add_btn = tk.Button(buttons_frame, text="+ Добавить", bg=self.colors['success'], 
                                fg='white', font=('Arial', 10, 'bold'),
                                command=self.add_task)
        self.add_btn.pack(fill='x', pady=2)
        
        self.delete_btn = tk.Button(buttons_frame, text="Удалить", bg=self.colors['danger'],
                                   fg='white', font=('Arial', 10, 'bold'),
                                   command=self.delete_task, state='disabled')
        self.delete_btn.pack(fill='x', pady=2)
        
        self.clear_btn = tk.Button(buttons_frame, text="Очистить", bg=self.colors['warning'],
                                  fg='white', font=('Arial', 10, 'bold'),
                                  command=self.clear_form)
        self.clear_btn.pack(fill='x', pady=2)
        
        extra_frame = tk.Frame(right_frame, bg='white')
        extra_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(extra_frame, text="👤 Новый пользователь", 
                 command=self.add_user_dialog,
                 bg=self.colors['info'], fg='white').pack(side='left', padx=2, fill='x', expand=True)
        
        tk.Button(extra_frame, text="Новая категория", 
                 command=self.add_category_dialog,
                 bg=self.colors['info'], fg='white').pack(side='left', padx=2, fill='x', expand=True)
        
        self.current_task_id = None
    
    def load_users(self):
        try:
            if 'users' in self.table_columns:
                columns = self.table_columns['users']
                print(f"Загрузка пользователей. Колонки: {columns}")
                
                id_col = 'id' if 'id' in columns else columns[0]  
                name_col = None
                for col in ['username', 'name', 'user_name', 'full_name']:
                    if col in columns:
                        name_col = col
                        break
                
                if name_col:
                    cursor = self.connection.cursor()
                    query = f"SELECT {id_col}, {name_col} FROM users ORDER BY {name_col}"
                    cursor.execute(query)
                    users = cursor.fetchall()
                    cursor.close()
                    
                    self.users = users
                    if users:
                        user_list = [f"{user[0]} - {user[1]}" for user in users]
                        self.user_combo['values'] = user_list
                        if len(user_list) > 0:
                            self.user_combo.current(0)
                    else:
                        self.user_combo['values'] = ['Нет пользователей']
                        self.user_combo.set('Нет пользователей')
                else:
                    self.user_combo['values'] = ['Ошибка: нет поля имени']
                    
        except Error as e:
            print(f"Ошибка загрузки пользователей: {e}")
            self.user_combo['values'] = [f'Ошибка: {e}']
    
    def load_categories(self):
        try:
            if 'categories' in self.table_columns:
                columns = self.table_columns['categories']
                print(f"Загрузка категорий. Колонки: {columns}")
                
                id_col = 'id' if 'id' in columns else columns[0]
                name_col = None
                for col in ['name', 'category_name', 'title']:
                    if col in columns:
                        name_col = col
                        break
                
                if name_col:
                    cursor = self.connection.cursor()
                    query = f"SELECT {id_col}, {name_col} FROM categories ORDER BY {name_col}"
                    cursor.execute(query)
                    categories = cursor.fetchall()
                    cursor.close()
                    
                    self.categories = categories
                    if categories:
                        cat_list = [f"{cat[0]} - {cat[1]}" for cat in categories]
                        self.category_combo['values'] = cat_list
                        if len(cat_list) > 0:
                            self.category_combo.current(0)
                    else:
                        self.category_combo['values'] = ['Нет категорий']
                        self.category_combo.set('Нет категорий')
                else:
                    self.category_combo['values'] = ['Ошибка: нет поля имени']
                    
        except Error as e:
            print(f"Ошибка загрузки категорий: {e}")
            self.category_combo['values'] = [f'Ошибка: {e}']
    
    def load_tasks(self):
        try:
            for item in self.tasks_tree.get_children():
                self.tasks_tree.delete(item)
            
            if 'tasks' not in self.table_columns:
                return
            
            task_columns = self.table_columns['tasks']
            print(f"Загрузка задач. Колонки tasks: {task_columns}")
            
            id_col = 'id' if 'id' in task_columns else task_columns[0]
            title_col = None
            for col in ['title', 'name', 'task_name', 'description']:
                if col in task_columns:
                    title_col = col
                    break
            
            status_col = None
            for col in ['status', 'task_status']:
                if col in task_columns:
                    status_col = col
                    break
            
            priority_col = None
            for col in ['priority', 'task_priority']:
                if col in task_columns:
                    priority_col = col
                    break
            
            date_col = None
            for col in ['due_date', 'deadline', 'date']:
                if col in task_columns:
                    date_col = col
                    break
            
            user_id_col = None
            for col in ['user_id', 'userid', 'userId', 'assigned_to']:
                if col in task_columns:
                    user_id_col = col
                    break
            
            category_id_col = None
            for col in ['category_id', 'cat_id', 'categoryId']:
                if col in task_columns:
                    category_id_col = col
                    break
            
            if title_col and status_col:
                cursor = self.connection.cursor()
                
                query = f"SELECT {id_col}, {title_col}, {status_col}"
                if priority_col:
                    query += f", {priority_col}"
                if date_col:
                    query += f", {date_col}"
                query += f" FROM tasks ORDER BY {id_col}"
                
                cursor.execute(query)
                tasks = cursor.fetchall()
                cursor.close()
                
                for task in tasks:
                    status = task[2] if len(task) > 2 else 'новая'
                    status_color = self.get_status_color(str(status).lower())
                    
                    values = [
                        task[0],  
                        task[1],  
                        task[2] if len(task) > 2 else '',  
                        task[3] if len(task) > 3 else '',  
                        task[4] if len(task) > 4 else '', 
                        'Без категории'  
                    ]
                    
                    self.tasks_tree.insert('', 'end', values=values[:6], tags=(status_color,))
                
                self.tasks_tree.tag_configure('red', foreground='red')
                self.tasks_tree.tag_configure('orange', foreground='orange')
                self.tasks_tree.tag_configure('green', foreground='green')
                self.tasks_tree.tag_configure('blue', foreground='blue')
                
        except Error as e:
            print(f"Ошибка загрузки задач: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить задачи:\n{e}")
    
    def get_status_color(self, status):
        colors = {
            'новая': 'blue',
            'new': 'blue',
            'в работе': 'orange',
            'in progress': 'orange',
            'завершена': 'green',
            'completed': 'green',
            'отложена': 'red',
            'deferred': 'red'
        }
        return colors.get(status, 'black')
    
    def on_task_select(self, event):
        selected = self.tasks_tree.selection()
        if selected:
            self.update_btn.config(state='normal')
            self.delete_btn.config(state='normal')
            
            item = self.tasks_tree.item(selected[0])
            task_id = item['values'][0]
            self.current_task_id = task_id
            print(f"Выбрана задача ID: {task_id}")
    
    def add_task(self):
        if not self.connection:
            messagebox.showerror("Ошибка", "Нет подключения к базе данных")
            return
        
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Предупреждение", "Введите название задачи")
            return
        
        try:
            task_columns = self.table_columns.get('tasks', [])
            
            insert_columns = []
            insert_values = []
            
            title_col = None
            for col in ['title', 'name', 'task_name']:
                if col in task_columns:
                    title_col = col
                    break
            
            if title_col:
                insert_columns.append(title_col)
                insert_values.append(title)
            
            desc_col = None
            for col in ['description', 'desc', 'task_description']:
                if col in task_columns:
                    desc_col = col
                    break
            
            if desc_col:
                insert_columns.append(desc_col)
                insert_values.append(self.desc_text.get(1.0, tk.END).strip())
            
            status_col = None
            for col in ['status', 'task_status']:
                if col in task_columns:
                    status_col = col
                    break
            
            if status_col:
                insert_columns.append(status_col)
                insert_values.append(self.status_var.get())
            
            priority_col = None
            for col in ['priority', 'task_priority']:
                if col in task_columns:
                    priority_col = col
                    break
            
            if priority_col:
                insert_columns.append(priority_col)
                insert_values.append(self.priority_var.get())
            
            date_col = None
            for col in ['due_date', 'deadline', 'task_date']:
                if col in task_columns:
                    date_col = col
                    break
            
            if date_col and self.due_entry.get().strip():
                insert_columns.append(date_col)
                insert_values.append(self.due_entry.get().strip())
            
            if not insert_columns:
                messagebox.showerror("Ошибка", "Не удалось определить структуру таблицы tasks")
                return
            
            placeholders = ', '.join(['%s'] * len(insert_columns))
            columns_str = ', '.join(insert_columns)
            query = f"INSERT INTO tasks ({columns_str}) VALUES ({placeholders})"
            
            print(f"Выполняется запрос: {query}")
            print(f"Значения: {insert_values}")
            
            cursor = self.connection.cursor()
            cursor.execute(query, insert_values)
            self.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Успех", "Задача успешно добавлена")
            self.clear_form()
            self.load_tasks()
            
        except Error as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить задачу:\n{e}")
    
    def update_task(self):
        if not self.current_task_id:
            return
        
        messagebox.showinfo("Информация", "Функция обновления в разработке")
    
    def delete_task(self):
        if not self.current_task_id:
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту задачу?"):
            try:
                cursor = self.connection.cursor()
                
                task_columns = self.table_columns.get('tasks', [])
                id_col = 'id' if 'id' in task_columns else task_columns[0]
                
                query = f"DELETE FROM tasks WHERE {id_col} = %s"
                cursor.execute(query, (self.current_task_id,))
                self.connection.commit()
                cursor.close()
                
                messagebox.showinfo("Успех", "Задача успешно удалена")
                self.clear_form()
                self.load_tasks()
                
            except Error as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить задачу:\n{e}")
    
    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete(1.0, tk.END)
        self.status_var.set('новая')
        self.priority_var.set('средний')
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        if hasattr(self, 'user_combo') and self.user_combo['values']:
            if len(self.user_combo['values']) > 0 and self.user_combo['values'][0] != 'Нет пользователей':
                self.user_combo.current(0)
        
        if hasattr(self, 'category_combo') and self.category_combo['values']:
            if len(self.category_combo['values']) > 0 and self.category_combo['values'][0] != 'Нет категорий':
                self.category_combo.current(0)
        
        self.current_task_id = None
        self.update_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
    
    def add_user_dialog(self):
        if not self.connection:
            messagebox.showerror("Ошибка", "Нет подключения к базе данных")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление пользователя")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        if 'users' in self.table_columns:
            columns = self.table_columns['users']
            
            entries = {}
            row = 0
            
            for col in columns:
                if col.lower() not in ['id', 'created_at', 'updated_at']:
                    tk.Label(dialog, text=f"{col}:").grid(row=row, column=0, padx=5, pady=5, sticky='w')
                    entry = tk.Entry(dialog, width=30)
                    entry.grid(row=row, column=1, padx=5, pady=5)
                    entries[col] = entry
                    row += 1
            
            def save_user():
                try:
                    insert_columns = []
                    insert_values = []
                    
                    for col, entry in entries.items():
                        value = entry.get().strip()
                        if value:
                            insert_columns.append(col)
                            insert_values.append(value)
                    
                    if not insert_columns:
                        messagebox.showwarning("Предупреждение", "Заполните хотя бы одно поле")
                        return
                    
                    placeholders = ', '.join(['%s'] * len(insert_columns))
                    columns_str = ', '.join(insert_columns)
                    query = f"INSERT INTO users ({columns_str}) VALUES ({placeholders})"
                    
                    cursor = self.connection.cursor()
                    cursor.execute(query, insert_values)
                    self.connection.commit()
                    cursor.close()
                    
                    messagebox.showinfo("Успех", "Пользователь добавлен")
                    dialog.destroy()
                    self.load_users()
                    
                except Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось добавить пользователя:\n{e}")
            
            tk.Button(dialog, text="Сохранить", command=save_user, 
                     bg='green', fg='white').grid(row=row, column=0, columnspan=2, pady=10)
    
    def add_category_dialog(self):
        if not self.connection:
            messagebox.showerror("Ошибка", "Нет подключения к базе данных")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление категории")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        if 'categories' in self.table_columns:
            columns = self.table_columns['categories']
            
            entries = {}
            row = 0
            
            for col in columns:
                if col.lower() not in ['id', 'created_at', 'updated_at']:
                    tk.Label(dialog, text=f"{col}:").grid(row=row, column=0, padx=5, pady=5, sticky='w')
                    entry = tk.Entry(dialog, width=30)
                    entry.grid(row=row, column=1, padx=5, pady=5)
                    
                    if 'color' in col.lower():
                        entry.insert(0, '#3498db')
                    
                    entries[col] = entry
                    row += 1
            
            def save_category():
                try:
                    insert_columns = []
                    insert_values = []
                    
                    for col, entry in entries.items():
                        value = entry.get().strip()
                        if value:
                            insert_columns.append(col)
                            insert_values.append(value)
                    
                    if not insert_columns:
                        messagebox.showwarning("Предупреждение", "Заполните хотя бы одно поле")
                        return
                    
                    placeholders = ', '.join(['%s'] * len(insert_columns))
                    columns_str = ', '.join(insert_columns)
                    query = f"INSERT INTO categories ({columns_str}) VALUES ({placeholders})"
                    
                    cursor = self.connection.cursor()
                    cursor.execute(query, insert_values)
                    self.connection.commit()
                    cursor.close()
                    
                    messagebox.showinfo("Успех", "Категория добавлена")
                    dialog.destroy()
                    self.load_categories()
                    
                except Error as e:
                    messagebox.showerror("Ошибка", f"Не удалось добавить категорию:\n{e}")
            
            tk.Button(dialog, text="Сохранить", command=save_category, 
                     bg='green', fg='white').grid(row=row, column=0, columnspan=2, pady=10)

def main():
    root = tk.Tk()
    app = TodoApp(root)
    
    def on_closing():
        if app.connection and app.connection.is_connected():
            app.connection.close()
            print("Соединение с БД закрыто")
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()