# Databricks notebook source
catalog = "<catalog_name>"
schema = "<schema_name>"
volume = "<volume_name>"
download_url = "https://health.data.ny.gov/api/views/jxy9-yhdk/rows.csv"
file_name = "rows.csv"
table_name = "<table_name>"
path_volume = "/Volumes/" + catalog + "/" + schema + "/" + volume
path_tables = catalog + "." + schema
print(path_tables) # Show the complete path
print(path_volume) # Show the complete path

# COMMAND ----------

dbutils.fs.cp(f"{download_url}", f"{path_volume}" + "/" + f"{file_name}")

# COMMAND ----------


