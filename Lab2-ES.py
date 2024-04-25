# Databricks notebook source
# Load the data from its source.
df = spark.read.load("/databricks-datasets/learning-spark-v2/people/people-10m.delta")

# Write the data to a table.
table_name = "people_10m"
df.write.saveAsTable(table_name)

# COMMAND ----------

display(spark.sql('DESCRIBE DETAIL people_10m_es'))

# COMMAND ----------

from delta.tables import DeltaTable

# Create table in the metastore
DeltaTable.createIfNotExists(spark) \
  .tableName("default.people10m_es") \
  .addColumn("id", "INT") \
  .addColumn("firstName", "STRING") \
  .addColumn("middleName", "STRING") \
  .addColumn("lastName", "STRING", comment = "surname") \
  .addColumn("gender", "STRING") \
  .addColumn("birthDate", "TIMESTAMP") \
  .addColumn("ssn", "STRING") \
  .addColumn("salary", "INT") \
  .execute()
  
# Create or replace table with path and add properties
DeltaTable.createOrReplace(spark) \
  .addColumn("id", "INT") \
  .addColumn("firstName", "STRING") \
  .addColumn("middleName", "STRING") \
  .addColumn("lastName", "STRING", comment = "surname") \
  .addColumn("gender", "STRING") \
  .addColumn("birthDate", "TIMESTAMP") \
  .addColumn("ssn", "STRING") \
  .addColumn("salary", "INT") \
  .property("description", "table with people data") \
  .location("/tmp/delta/people10m") \
  .execute()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW people_updates (
# MAGIC   id, firstName, middleName, lastName, gender, birthDate, ssn, salary
# MAGIC ) AS VALUES
# MAGIC   (9999998, 'Billy', 'Tommie', 'Luppitt', 'M', '1992-09-17T04:00:00.000+0000', '953-38-9452', 55250),
# MAGIC   (9999999, 'Elias', 'Cyril', 'Leadbetter', 'M', '1984-05-22T04:00:00.000+0000', '906-51-2137', 48500),
# MAGIC   (10000000, 'Joshua', 'Chas', 'Broggio', 'M', '1968-07-22T04:00:00.000+0000', '988-61-6247', 90000),
# MAGIC   (20000001, 'John', '', 'Doe', 'M', '1978-01-14T04:00:00.000+000', '345-67-8901', 55500),
# MAGIC   (20000002, 'Mary', '', 'Smith', 'F', '1982-10-29T01:00:00.000+000', '456-78-9012', 98250),
# MAGIC   (20000003, 'Jane', '', 'Doe', 'F', '1981-06-25T04:00:00.000+000', '567-89-0123', 89900);
# MAGIC
# MAGIC MERGE INTO people_10m
# MAGIC USING people_updates
# MAGIC ON people_10m.id = people_updates.id
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM people_10m WHERE id >= 9999998

# COMMAND ----------

people_df = spark.read.table(table_name)

display(people_df)

## or people_df = spark.read.load(table_path)

#display(people_df)

# COMMAND ----------

df.write.mode("append").saveAsTable("people10m")

# COMMAND ----------

df.write.mode("overwrite").saveAsTable("people10m")

# COMMAND ----------

from delta.tables import *
from pyspark.sql.functions import *

deltaTable = DeltaTable.forPath(spark, '/tmp/delta/people-10m')

# Declare the predicate by using a SQL-formatted string.
deltaTable.update(
  condition = "gender = 'F'",
  set = { "gender": "'Female'" }
)

# Declare the predicate by using Spark SQL functions.
deltaTable.update(
  condition = col('gender') == 'M',
  set = { 'gender': lit('Male') }
)

# COMMAND ----------

from delta.tables import *
from pyspark.sql.functions import *

deltaTable = DeltaTable.forPath(spark, '/tmp/delta/people-10m')

# Declare the predicate by using a SQL-formatted string.
deltaTable.delete("birthDate < '1955-01-01'")

# Declare the predicate by using Spark SQL functions.
deltaTable.delete(col('birthDate') < '1960-01-01')

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY people_10m

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM people_10m VERSION AS OF 0

# COMMAND ----------

df2 = spark.read.format('delta').option('versionAsOf', 0).table("people_10m")

display(df2)

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE people_10m

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE people_10m
# MAGIC ZORDER BY (gender)

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM people_10m

# COMMAND ----------


