from tasks.basic_task import BaseTask, app


class BasicAnalyzeTask(BaseTask):
    # ToDo: here will be overridden functions: on_prerun, run, on_success
    pass


app.tasks.register(BasicAnalyzeTask())
