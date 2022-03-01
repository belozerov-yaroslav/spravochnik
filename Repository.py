import sqlite3
from random import choice
from Task import Task
from Source import Source
from Illustration import Illustration


class Repository:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_task(self, task_id):
        con = sqlite3.connect(self.base_path)
        cur = con.cursor()
        task_inf = cur.execute("SELECT * FROM tasks WHERE id=(?)", (task_id,)).fetchone()
        images = cur.execute("SELECT * FROM images WHERE task=(?)", (task_id,)).fetchall()
        illustrations = [Illustration(image[0], image[1], image[2], image[3]) for image in images]
        illustrations_id = {illustrations[i].base_id: illustrations[i] for i in range(len(illustrations))}
        task_source = None
        if task_inf[5] is not None:
            source_inf = cur.execute("SELECT * FROM sources WHERE id=(?)", (task_inf[5])).fetchall()[0]
            task_source = Source(source_inf[0], source_inf[1])
        return Task(task_inf[0], task_inf[1], illustrations_id, task_inf[2],
                    task_inf[3], task_inf[4], task_source, task_inf[6])

    def get_random_task(self, task_number):
        con = sqlite3.connect(self.base_path)
        cur = con.cursor()
        random_id = choice(cur.execute("SELECT id FROM tasks WHERE number=(?)", (task_number,)).fetchall())[0]
        print(random_id)
        return self.get_task(random_id)

    def get_all_number_tasks(self, number):
        con = sqlite3.connect(self.base_path)
        cur = con.cursor()
        tasks = []
        ids_of_number = cur.execute("SELECT id FROM tasks WHERE number=(?)", (number,)).fetchall()
        ids_of_number = list(map(lambda element: element[0], ids_of_number))
        for number_id in ids_of_number:
            tasks.append(self.get_task(number_id))
        return tasks

    def get_all_source_tasks(self, source_id):
        con = sqlite3.connect(self.base_path)
        cur = con.cursor()
        tasks = []
        ids_of_source = cur.execute("SELECT id FROM tasks WHERE source=(?)", (source_id,)).fetchall()
        ids_of_source = list(map(lambda element: element[0], ids_of_source))
        for task_id in ids_of_source:
            tasks.append(self.get_task(task_id))
        return sorted(tasks, key=lambda element: element.number)
