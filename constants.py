#page constants
CURRENT_PAGE = "currentpage"
ENRTY = "entry"
START_SHIFT = "startshift"
PROMPTS = "prompts"
WORKERS = "workers"
WAITING_FOR_FRIEND = "waiting-for-friend"
CONTACT = "contact"
SELECT_PROMPT = "select-prompt"
COMPLETE = "complete"

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

worker_log_index = "logIndex"
worker_timesheet_index = "timesheetIndex"
workers_config_columns_names = [workers_name,
                                worker_contact,
                                worker_is_working,
                                worker_log_index,
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

worker_log_df_key="log"
worker_log_time_contact="timeContact"
worker_log_time_prompt="timePrompt"
worker_log_time_finished="timeFinished"
worker_log_prompt="prompt"
worker_log_rating="rating"
worker_log_notes="notes"
worker_log_column_names = [worker_log_time_contact,
                           worker_log_time_prompt,
                           worker_log_time_finished,
                           worker_log_prompt,
                           worker_log_rating,
                           worker_log_notes]

prompts_table = "prompts"
prompts_table_name = "prompts"
prompts_key_column_name = "prompts"
prompts_key = "prompts"
prompts_column_name = "prompts"
prompts_dataframe_key_name = "prompts_dataframe"
prompts_item_name = "prompts"
prompts_config_columns_names = [prompts_column_name, timestamp_str]
