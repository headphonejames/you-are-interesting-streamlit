import streamlit as st
from lib import google_sheets_funcs as gsheets
from lib import df_funcs as df_func

description = "Question management"
questions_table_name = "questions"
questions_label_name = "questions"
questions_column_name = "questions"
questions_key_name = "questions"
questions_df_key = "questions_dataframe"
def run():
    #constants

    if 'modded' not in st.session_state:
        st.session_state.modded = False

    # initialize dataframe
    if questions_df_key not in st.session_state:
        df_func.set_df(st, questions_df_key, gsheets.load_the_table(questions_table_name))

    # initialize question list
    if not questions_column_name in df_func.get_df(st, questions_df_key):
        # add questions colum to datatabe
        updated_df = df_func.get_df(st, questions_df_key)[questions_column_name] = []
        df_func.set_df(st, questions_df_key,updated_df)

    def remove_question(question, index):
        df = df_func.get_df(st, questions_df_key)
        #Remove question from list in data table
        new_df = df_func.remove_col(df, index)
        df_func.set_df(st, questions_df_key, new_df)
        st.session_state.modded = True
        # set_df(st, df_func.remove_col(df_func.get_df(st, questions_df_key), index))

    def clear_state(df):
        df_func.set_df(st, questions_df_key, df)
        st.session_state.questions_key = ''
        st.session_state.modded = True

    def add_question():
        df = df_func.get_df(st, questions_df_key)
        question = st.session_state.questions_key
        # check if questions already exists
        if not question in df[questions_column_name].tolist():
            #update datatable
            df = df_func.add_col(df, [question])
            clear_state(df)

    st.title('Prompts for connection')

    index = 0
    df = df_func.get_df(st, questions_df_key)
    if "questions" in df:
        for question in df["questions"]:
            index = index + 1
            st.checkbox(question, key="id_{}".format(question),  on_change=remove_question, args=(question, index, ))

    st.session_state.question_name = ''
    st.text_input(label=questions_label_name, placeholder=questions_label_name, on_change=add_question, key='questions_key')


    def done():
        # update sheet
        gsheets.update_the_table(df_func.get_df(st, questions_df_key), questions_table_name)
        st.session_state.modded = False

    st.button("submit", on_click=done, disabled=(not st.session_state.modded))

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()