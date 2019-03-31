from tasks.basic_task import BaseTask, app


class BasicAnalyzeTask(BaseTask):
    pass


app.tasks.register(BasicAnalyzeTask())
