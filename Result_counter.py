class Result_counter:
    @staticmethod
    def check_task(task, answer):
        if task.number < 26:
            if task.answer == answer:
                return 1
        else:
            if task.answer == answer:
                return 2
            if task.answer.split()[::-1] == answer.split():
                return 1
            if len(answer.split()) == 2 and (answer.split()[0] in task.answer.split() or
                                             answer.split()[1] in task.answer.split()):
                return 1
            if len(answer.split()) == 1 and answer in task.answer.split():
                return 1
        return 0

    @staticmethod
    def count_result(tasks, answers):
        counter = 0
        for task_num in range(len(tasks)):
            counter += Result_counter.check_task(tasks[task_num], answers[task_num])
        return counter
