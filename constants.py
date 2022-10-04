#page constants
CURRENT_PAGE = "currentpage"
ENRTY = "entry"
START_SHIFT = "startshift"
PROMPTS = "prompts"
WORKERS = "workers"
WAITING_FOR_FRIEND = "waiting-for-friend"


modded_key = "modded"

workers_table = "workers"
workers_table_name = "workers"
workers_label_name = "workers"
workers_name = "workers-name"
workers_name_cached = "wrname-cache"
workers_key = "name"
worker_is_working = "isWorking"
is_display_column = "isDisplayColumn"
default_value = "default"
timestamp_str = "timeStamp"
worker_contact = "contact"
worker_connection_index = "connectionIndex"
worker_timesheet_index = "timesheetIndex"
workers_config_columns_names = [workers_name,
                                worker_contact,
                                worker_is_working,
                                worker_connection_index,
                                worker_timesheet_index,
                                timestamp_str]
workers_df_key = "workers-df"
workers_item_name = "workers"
st_data_key = "data"
worksheets_df_key = "worksheets"

worker_timesheet_df_key="timesheet"
worker_shift_start="start"
worker_shift_stop="stop"
worker_shift_column_names = [worker_shift_start, worker_shift_stop]
worker_index = "worker_index"

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


prompts_table = "prompts"
prompts_table_name = "prompts"
prompts_key_column_name = "prompts"
prompts_key = "prompts"
prompts_column_name = "prompts"
prompts_dataframe_key_name = "prompts_dataframe"
prompts_item_name = "prompts"
prompts_config_columns_names = [prompts_column_name, timestamp_str]
