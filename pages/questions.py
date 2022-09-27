from itemslist import execute

questions_table_name = "questions"
questions_label_name = "A prompt or question"
questions_column_name = "questions"
questions_dataframe_key_name = "questions_dataframe"
title = "Prompts from connections"
item_name = "questions"
question_input_key = "questions_input"

def run():
    execute(questions_dataframe_key_name,
            questions_table_name,
            questions_label_name,
            questions_column_name,
            title,
            item_name,
            question_input_key)

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()