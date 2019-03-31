from tasks.basic_task import BaseTask, app


class CheckTextSources(BaseTask):
    pass


class GetDocumentText(BaseTask):
    pass


app.tasks.register(CheckTextSources())
app.tasks.register(GetDocumentText())
