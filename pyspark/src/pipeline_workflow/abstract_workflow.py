from abc import abstractmethod, ABC 

class AbstractWorkflow(ABC):
    def __init__(self,params,spark):
        self.params = params
        self.spark = spark
        self.steps = {
            'txt' : ['pipeline_read_txt', 'pipeline_transform_txt', 'pipeline_save_txt']
            ,'linkedln' : ['pipeline_read_linkedln', 'pipeline_transform_linkedln', 'pipeline_save_linkedln']
        }
    @abstractmethod
    def run(self):
        pass

    def get_config(self,file_type):
        return self.steps[file_type]