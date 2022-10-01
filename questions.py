from crud_items_list import execute

prompts_table_name = "prompts"
prompts_label_name = "A prompt or prompt"
prompts_column_name = "prompts"
prompts_dataframe_key_name = "prompts_dataframe"
title = "Prompts from connections"
item_name = "prompts"
prompt_input_key = "prompts_input"

def run():
    execute(prompts_dataframe_key_name,
            prompts_table_name,
            prompts_label_name,
            prompts_column_name,
            title,
            item_name,
            prompt_input_key)

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()