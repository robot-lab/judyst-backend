from tasks.basic_task import BaseTask, app


class AnalyzeTasksGeneration(BaseTask):
    pass


app.tasks.register(AnalyzeTasksGeneration())
