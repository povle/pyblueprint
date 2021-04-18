from . import AbstractBlock


class ProcessingBlock(AbstractBlock):
    def __init__(self, function, pos=(0, 0), parent=None):
        super().__init__(uifile='./ui/ProcessingBlock.ui',
                         function=function,
                         pos=pos,
                         parent=parent,
                         special_args=['path'])

    def processData(self, data):
        return self.executeFunction(data=data)
