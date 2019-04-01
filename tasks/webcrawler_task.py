from tasks.basic_task import BaseTask, app


class CheckTextSources(BaseTask):
    # ToDo: here will be overridden functions: on_prerun, run, on_success
    pass


class GetDocumentText(BaseTask):
    # ToDo: here will be overridden functions: on_prerun, run, on_success
    pass


app.tasks.register(CheckTextSources())
app.tasks.register(GetDocumentText())
