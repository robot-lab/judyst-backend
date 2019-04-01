from tasks.basic_task import BaseTask, app


class AnalyzeTasksGeneration(BaseTask):
    # ToDo: here will be override functions: on_prerun, run, on_success
    pass


class AddNewFile(BaseTask):
    # ToDo: here will be override functions: on_prerun, run, on_success
    pass


app.tasks.register(AnalyzeTasksGeneration())
app.tasks.register(AddNewFile())
