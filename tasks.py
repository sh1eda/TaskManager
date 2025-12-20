import datetime
from storage import Storage

class Task:
    def __init__(self, id, title, description, category, priority, due_date, created_date, updated_date, status="Pending..."):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.created_date = created_date
        self.updated_date = updated_date
        self.status = status

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            title=data.get("task"),
            description=data.get("description"),
            category=data.get("category"),
            priority=data.get("priority"),
            due_date=data.get("due"),
            created_date=data.get("created"),
            updated_date=data.get("updated"),
            status=data.get("status")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "task": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "due": self.due_date,
            "created": self.created_date,
            "updated": self.updated_date,
            "status": self.status
        }
    
    def __str__(self):
        return f"{self.title} (Status: {self.status})"


class TaskManager:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        data = self.storage.load_data()
        return [Task.from_dict(t) for t in data]

    def _save_tasks(self):
        data = [t.to_dict() for t in self.tasks]
        self.storage.save_data(data)

    def add_task(self, title, description, category, priority, due_date):
        new_id = len(self.tasks) + 1
        today = str(datetime.date.today())
        
        new_task = Task(
            id=new_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date,
            created_date=today,
            updated_date=today
        )
        
        self.tasks.append(new_task)
        self._save_tasks()
        return new_task

    def get_all_tasks(self):
        return self.tasks

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            self._save_tasks()
            return removed_task
        return None

    def update_task_status(self, index, new_status):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.status = new_status
            task.updated_date = str(datetime.date.today())
            self._save_tasks()
            return task
        return None

