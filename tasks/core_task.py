from tasks.basic_task import BaseTask, app


class AnalyzeTasksGeneration(BaseTask):
    pass


class AddNewFile(BaseTask):
    pass


app.tasks.register(AnalyzeTasksGeneration())
app.tasks.register(AddNewFile())
