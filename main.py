from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from tasks import TaskManager
from storage import Storage
from views import TaskView

import os
import time

console = Console()

def make_header():
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right")
    grid.add_row(
        "[white]Personal Task Manager[/]",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    return Panel(grid)

def make_footer():
    menu_text = (
        "[bold cyan][1][/] Manage Tasks  "
        "[bold cyan][2][/] Filter View  "
        "[bold cyan][3][/] Search Task  "
        "[bold cyan][4][/] Exit"
    )
    return Panel(Align.center(menu_text), title="Menu")

def make_task_table(tasks):
    table = Table(expand=True, border_style="bright_black")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True, width=4)
    table.add_column("Task", style="magenta", ratio=3)
    table.add_column("Category", style="blue", ratio=1)
    table.add_column("Priority", justify="center", style="green", width=8)
    table.add_column("Due Date", justify="center", style="yellow", width=12)
    table.add_column("Status", justify="center", width=12)

    if not tasks:
        table.add_row("", "No tasks found", "", "", "", "")
        return table

    for index, task in enumerate(tasks, start=1):
        status_style = "green" if task.status.lower() in ["completed", "done"] else "red"
        status_text = f"[{status_style}]{task.status.title()}[/]"
        table.add_row(
            str(index),
            task.title,
            task.category,
            str(task.priority),
            task.due_date,
            status_text
        )
    return table

def make_layout():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    return layout

def check_upcoming_deadlines(manager, console):
    tasks = manager.get_all_tasks()
    today = datetime.now().date()
    warnings = []

    for task in tasks:
        if task.status.lower() in ["completed", "done"]:
            continue
        
        try:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
            delta = (due_date - today).days
            
            if 0 <= delta <= 2:
                warnings.append(f"[bold]{task.title}[/] (Due: {task.due_date})")
            if delta < 0:
                warnings.append(f"[bold]{task.title}[/] (Overdue: {task.due_date})")
                
        except ValueError:
            continue

    if warnings:
        warning_text = "\n".join(warnings)
        panel = Panel(
            Align.center(f"[bold red]WARNING: The following tasks are due soon![/]\n\n{warning_text}"),
            title="[bold red]Upcoming Deadlines[/]",
            border_style="red"
        )
        console.print(panel)
        time.sleep(3)
        console.clear()

def main():
    storage = Storage("./data/tasks.json")
    manager = TaskManager(storage)
    
    manager.check_overdue_tasks()
    
    view = TaskView()
    
    current_filters = {
        "category": None,
        "priority": None,
        "start_date": None,
        "end_date": None
    }
    
    layout = make_layout()
    layout["header"].update(make_header())
    layout["footer"].update(make_footer())

    check_upcoming_deadlines(manager, console)

    with Live(layout, screen=True, refresh_per_second=4) as live:
        while True:
            if any(current_filters.values()):
                tasks = view.filter_tasks(
                    manager.get_all_tasks(),
                    category=current_filters["category"],
                    priority=current_filters["priority"],
                    start_date=current_filters["start_date"],
                    end_date=current_filters["end_date"]
                )
                filter_text = []
                if current_filters["category"]: filter_text.append(f"Cat: {current_filters['category']}")
                if current_filters["priority"]: filter_text.append(f"Prio: {current_filters['priority']}")
                if current_filters["start_date"]: filter_text.append(f"From: {current_filters['start_date']}")
                if current_filters["end_date"]: filter_text.append(f"To: {current_filters['end_date']}")
                title = f"Tasks (Filtered: {', '.join(filter_text)})"
            else:
                tasks = manager.get_all_tasks()
                title = "Tasks"

            layout["header"].update(make_header())
            layout["body"].update(Panel(make_task_table(tasks), title=title))
            
            try:
                live.stop()
                console.clear() 
                console.print(make_header())
                console.print(Panel(make_task_table(tasks), title=title))
                console.print(make_footer())
                
                choice = Prompt.ask("\nChoose an option [1-4]", choices=["1", "2", "3", "4"], default="4")
                
                if choice == "1":
                    menu_text = (
                        "[bold cyan][1][/] Add Task  "
                        "[bold cyan][2][/] Delete Task  "
                        "[bold cyan][3][/] Update Status  "
                        "[bold cyan][4][/] Back to Main Menu"
                    )
                    console.print(Panel(Align.center(menu_text), title="Manage Tasks"))
                    sub = Prompt.ask("Manage Option", choices=["1", "2", "3", "4"], default="4")
                    if sub == "1":
                        console.print("Add Task")
                        console.rule("[bold blue]Add New Task[/]")
                        name = Prompt.ask("Task Name")
                        desc = Prompt.ask("Description", default="No description")
                        cat = Prompt.ask("Category", default="General")
                        prio = IntPrompt.ask("Priority", default=1)
                        due = Prompt.ask("Due Date", default=str(datetime.now().date()))
                        manager.add_task(name, desc, cat, prio, due)
                        console.print("[green]Task Added![/]")
                        time.sleep(1)

                    elif sub == "2":
                        if any(current_filters.values()):
                            console.rule("[bold red]Cannot delete while filtered. Clear filters first.[/]")

                        elif not tasks:
                            console.rule("[bold red]No tasks found![/]", style="red")
                            time.sleep(1)
                            continue
                        else:
                            console.rule("[bold red]Delete Task[/]")
                            idx = IntPrompt.ask("Task ID to delete", default=1)
                            if idx > 0:
                                res = manager.delete_task(idx-1)
                                if res: console.print(f"[red]Deleted {res.title}[/]")
                                else: console.print("[red]Invalid ID[/]")
                        time.sleep(1)
                        
                    elif sub == "3":
                        if any(current_filters.values()):
                            console.rule("[bold red]Cannot update while filtered. Clear filters first.[/]", style="red")
                        elif not tasks:
                            console.rule("[bold red]No tasks found![/]", style="red")
                            time.sleep(1)
                            continue
                        else:
                            console.rule("[bold yellow]Update Status[/]")
                            idx = IntPrompt.ask("Task ID to update", default=1)
                            if idx > 0 and idx <= len(tasks):
                                stat = Prompt.ask("New Status")
                                if stat not in ["Pending", "In Progress", "Completed", "Overdue"]:
                                    console.print("[red]Invalid Status (Pending, In Progress, Completed, Overdue)[/]")
                                    time.sleep(3)
                                    continue
                                if stat == "Overdue":
                                    console.print("[red]Overdue status cannot be set manually.[/]")
                                    time.sleep(1)
                                    continue
                                if stat == "Completed":
                                    console.print("[red]Completed status cannot be set manually.[/]")
                                    time.sleep(1)
                                    continue
                                manager.update_task_status(idx-1, stat)
                                console.print("[green]Updated![/]")
                            else:
                                console.print("[red]Invalid ID[/]")
                            time.sleep(2)
                        
                    elif sub == "4":
                        console.print("Going Back to Main Menu")
                        continue

                elif choice == "2":
                    if not tasks:
                        console.rule("[bold red]No tasks found![/]", style="red")
                        time.sleep(1)
                        continue
                    console.rule("[bold magenta]Filter Tasks[/]")
                    console.print("1. Filter by Category")
                    console.print("2. Filter by Priority")
                    console.print("3. Filter by Date Range")
                    console.print("4. Clear Filters")
                    
                    sub = Prompt.ask("Filter Option", choices=["1", "2", "3", "4"], default="4")
                    if sub == "1":
                        current_filters["category"] = Prompt.ask("Enter Category")
                    elif sub == "2":
                        current_filters["priority"] = IntPrompt.ask("Enter Priority")
                    elif sub == "3":
                         s_date = Prompt.ask("Start Date (YYYY-MM-DD)", default=None)
                         e_date = Prompt.ask("End Date (YYYY-MM-DD)", default=None)
                         if s_date:
                             try:
                                 current_filters["start_date"] = datetime.strptime(s_date, "%Y-%m-%d").date()
                             except ValueError: console.print("[red]Invalid Start Date[/]")
                         if e_date:
                             try:
                                 current_filters["end_date"] = datetime.strptime(e_date, "%Y-%m-%d").date()
                             except ValueError: console.print("[red]Invalid End Date[/]")
                    elif sub == "4":
                        current_filters = {k: None for k in current_filters}
                        console.print("[yellow]Filters Cleared[/]")
                    
                    time.sleep(0.5)

                elif choice == "3":
                    if not tasks:
                        console.rule("[bold red]No tasks found![/]", style="red")
                        time.sleep(1)
                        continue

                    console.rule("[bold blue]Search Task[/]")
                    search_term = Prompt.ask("Search Term")
                    tasks = view.search_tasks(manager.get_all_tasks(), search_term)
                    console.print(make_task_table(tasks))
                    time.sleep(1)

                elif choice == "4":
                    console.rule("[#7CFF5E]Goodbye![/]", style="#7CFF5E")
                    break
                    
                live.start()
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()