import datetime

class TaskView:
    def filter_tasks(self, tasks, category=None, priority=None, start_date=None, end_date=None):
        filtered = tasks
        
        if category:
            filtered = [t for t in filtered if t.category.lower() == category.lower()]
        
        if priority is not None:
             filtered = [t for t in filtered if str(t.priority) == str(priority)]
        
        if start_date or end_date:
            filtered_by_date = []
            for t in filtered:
                try:
                    task_date = datetime.datetime.strptime(t.due_date, "%Y-%m-%d").date()
                    
                    if start_date and task_date < start_date:
                        continue
                    if end_date and task_date > end_date:
                        continue
                    filtered_by_date.append(t)
                except ValueError:
                    continue 
            filtered = filtered_by_date
            
        return filtered

    def search_tasks(self, tasks, search_term):
        return [t for t in tasks if search_term.lower() in t.title.lower()]
