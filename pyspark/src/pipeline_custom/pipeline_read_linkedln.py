from pipeline_step.pipeline_step import PipelineStep

class PipelineReadLinkedln(PipelineStep):
    def __init__(self):
        super().__init__()
        print("Read File")
    def run(self, spark, params, df):
        path = params.args['input_path']
        df = spark.read.option("inferSchema",True).json(path)
        return df