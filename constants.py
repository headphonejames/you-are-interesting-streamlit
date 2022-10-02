#page constants
CURRENT_PAGE = "currentpage"
ENRTY = "entry"
START_SHIFT = "startshift"
PROMPTS = "prompts"
WORKERS = "workers"

workers_table = "workers"
workers_table_name = "workers"
workers_label_name = "workers"
workers_name = "name"
workers_key = "name"
worker_is_working = "isWorking"
is_display_column = "isDisplayColumn"
default_value = "default"
timestamp_str = "timeStamp"
workers_config_columns_names = [workers_name, "contact", worker_is_working, timestamp_str]
workers_dataframe_key_name = "workersDataframe"
workers_item_name = "workers"
st_data_key = "data"

worker_initiated_contact_ts="contactTimeStamp"
worker_initiated_prompt_ts="promptTimeStamp"
worker_finished_interation_ts="finishedTimeStamp"
worker_convo_ranking="converstaionQuality"
worker_convo_notes="notes"
worker_prompt_choice="prompt"
worker_column_names = [worker_initiated_contact_ts,
                       worker_initiated_prompt_ts,
                       worker_finished_interation_ts,
                       worker_convo_ranking,
                       worker_convo_notes,
                       worker_prompt_choice
                       ]

worker_shift_start="workerShiftStartTimeStamp"
worker_shift_stop="workerShiftStopTimeStamp"
worker_shift_column_names = [worker_shift_start, worker_shift_stop]

prompts_table = "prompts"
prompts_table_name = "prompts"
prompts_label_name = "prompts"
prompts_column_name = "prompts"
prompts_dataframe_key_name = "prompts_dataframe"
prompts_item_name = "prompts"
