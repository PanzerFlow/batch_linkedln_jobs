import abc

class PipelineStep(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self) :
        print("Initialize construction")

    @abc.abstractclassmethod
    def run(sef,*args):
        pass
