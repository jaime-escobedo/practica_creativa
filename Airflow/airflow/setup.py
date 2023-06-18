import sys, os, re

from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta
import iso8601

PROJECT_HOME = os.getenv("PROJECT_HOME")

# En estas propiedades iniciales se define el numero de intentos que debe 
# realizar el DAG antes de que no se ejecute y muera con la propiedad retries
#(3 en este caso).
# Se indica desde la fecha por la que debe comenzar("2016-12-01").
# Y,finalmente,con retry_delay se define cada cuanto tiempo se realizan los 
# reintentos(5min en este caso).
# 'depends_on_past': False, significa que esta esta ejecucion del DAG no depende de que se hayan realizado
# las tareas anteriores satisfactoriamente
default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': iso8601.parse_date("2016-12-01"),
  'retries': 3,
  'retry_delay': timedelta(minutes=5),
}

# En esta parte se configura el DAG con las propiedades definidas anteriormente
# y sele da un nombre. También se le asigna un schedule_interval para definir 
# cada cuanto tiempo se debe realizar este DAG. Otros posibles valores del schedule_interval
#son: @once @hourly @daily
training_dag = DAG(
  'agile_data_science_batch_prediction_model_training',
  default_args=default_args,
  schedule_interval=None
)

# We use the same two commands for all our PySpark tasks
pyspark_bash_command = """
/opt/spark/bin/spark-submit --master {{ params.master }} \
  {{ params.base_path }}/{{ params.filename }} \
  {{ params.base_path }}
"""
pyspark_date_bash_command = """
/opt/spark/bin/spark-submit --master {{ params.master }} \
  {{ params.base_path }}/{{ params.filename }} \
  {{ ts }} {{ params.base_path }}
"""


# Gather the training data for our classifier
"""
extract_features_operator = BashOperator(
  task_id = "pyspark_extract_features",
  bash_command = pyspark_bash_command,
  params = {
    "master": "local[8]",
    "filename": "resources/extract_features.py",
    "base_path": "{}/".format(PROJECT_HOME)
  },
  dag=training_dag
)
"""

# Aqui se define el BashOperator con el que se determina que tarea se va a ejecutar 
# en el DAG. Dentro se definen la dirección del master de Spark("local[8]"), 
#el archivo de entrenamiento ("resources/train_spark_mllib_model.py")
# y la direccioón del proyecto("{}/".format(PROJECT_HOME))

# Train and persist the classifier model
train_classifier_model_operator = BashOperator(
  task_id = "pyspark_train_classifier_model",
  bash_command = pyspark_bash_command,
  params = {
  #Para asignar el master a un spark node que sea master se ha cambiado el campo "master": "local[8]" por:
    "master": "spark://master:7077",
    "filename": "resources/train_spark_mllib_model.py",
    "base_path": "{}".format(PROJECT_HOME)
  },
  dag=training_dag
)

# The model training depends on the feature extraction
#train_classifier_model_operator.set_upstream(extract_features_operator)
