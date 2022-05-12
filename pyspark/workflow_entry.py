import argparse
import ast
from pipeline_workflow.default_workflow import DefaultWorkflow
from pipeline_utils.package import SparkParams
from pyspark.sql import SparkSession

"""
Spark submit example:
To build the artifact
zip -r job.zip . && cp job.zip ~/data/ && cp ../workflow_entry.py ~/data/

docker run -dit --name pyspark -v /home/eguo/data:/data -v /home/eguo/spark-repo:/spark-repo jupyter/pyspark-notebook
spark-submit --master local --py-files /data/job.zip /data/workflow_entry.py -p "{'input_path':'/data/banking.csv','name':'demo', 'file_type':'txt', 'output_path':'/data/pyspark', 'partition_column': 'job'}"
"""

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--params", required=True, help="Spark input parameters, {file_type:txt,input_path:s3://........}")
args = parser.parse_args()

print('args ' + str(args))

def parse_command_line(args):
    """Convert a command line argument to a dict
        {"file_type:txt,input_path:s3.....}
    """
    return ast.literal_eval(args)

def spark_init(parser_name):
    """
    To initiallize sparkSession 
    """
    ss = SparkSession \
        .builder \
        .appName(parser_name) \
        .getOrCreate()
    ss.sparkContext.setLogLevel("ERROR")
    return ss

params = parse_command_line(args.params)
print('runnung stuff ' + str(params))
params = SparkParams(params)
spark = spark_init(params.args['name'])

if __name__ == "__main__":
    '''
    checking if the script is being run via command 'python script'
    '''
    print("Executing script via python")
    #spark.read.parquet('file:/data/wcd').show()
    dataflow = DefaultWorkflow(params, spark)
    #spark.sparkContext.getConf().getAll()
    dataflow.run()
else:
    print("Importing script")