from flask import Flask, render_template, request, redirect, send_file
from Repository import Repository
from random import choice
from Result_counter import Result_counter

app = Flask(__name__)
repository = Repository("tasks.db")


@app.route("/")
@app.route("/main")
def main_page():
    return render_template('main.html')


@app.route("/variant", methods=['GET', 'POST'])
def variant_page():
    if request.method == "POST":
        answers = []
        tasks = []
        for taskNumber in range(1, 28):
            answers.append(request.form[f"answer{taskNumber}"])
            tasks.append(repository.get_task(int(request.form[f"taskId{taskNumber}"])))
        return render_template("variant_results.html", tasks=tasks, answers=answers,
                               result=Result_counter.count_result(tasks, answers))
    tasks = [choice(repository.get_all_number_tasks(i)) for i in range(1, 28)]
    return render_template('task_to_check.html', tasks=tasks, page_title=f"Тренировочный вариант ЕГЭ", for_check=True)


@app.route("/training", methods=['GET', 'POST'])
def training_page():
    if request.method == "POST":
        try:
            number = int(request.form["search"])
            return redirect(f"number/{number}")
        except Exception:
            return render_template("training.html", message="Необходимо ввести число!")
    return render_template("training.html", message="")


@app.route('/download/task_files/<int:task_id>')
def download_task_files(task_id):
    path = "static/task_files/" + repository.get_task(task_id).files
    if path:
        return send_file(path, as_attachment=True)
    else:
        return "bad request!", 404


@app.route("/training/<int:number>")
def train_number(number):
    return render_template("tasks_with_answer.html",
                           tasks=repository.get_all_number_tasks(number),
                           page_title=f"Все задания {number}")


@app.route("/number/<int:task_id>")
def number_page(task_id):
    return render_template("tasks_with_answer.html", tasks=[repository.get_task(task_id)],
                           page_title="Поиск номера")


@app.route("/source/<int:source_id>")
def source_page(source_id):
    return render_template("source.html", tasks=repository.get_all_source_tasks(source_id),
                           page_title="Все задания из источника", for_check=False)


@app.route("/structure")
def structure_page():
    return render_template('structure.html')


@app.route("/ege_help")
def ege_help():
    return render_template('ege_help.html')


@app.route("/helpful_links")
def helpful_links():
    return render_template('helpful_links.html')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
