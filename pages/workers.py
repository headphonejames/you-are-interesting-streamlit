from itemslist import execute

workers_table_name = "workers"
workers_label_name = "workers"
workers_column_name = "workers"
workers_dataframe_key_name = "workers_dataframe"
title = "Name of staff"
item_name = "workers"
worker_input_key = "workers_input"

def run():
    execute(workers_dataframe_key_name,
            workers_table_name,
            workers_label_name,
            workers_column_name,
            title,
            item_name,
            worker_input_key)

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()