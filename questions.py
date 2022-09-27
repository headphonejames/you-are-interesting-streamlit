import streamlit as st
import pandas as pd


if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []


class NewStudent:
    def __init__(self, page_id):
        st.title(f"Student N°{page_id}")
        self.name = st.text_input("Name")
        self.age = st.text_input("Age")


def main():
    placeholder = st.empty()
    placeholder2 = st.empty()

    while True:
        num = st.session_state.num

        if placeholder2.button('end', key=num):
            placeholder2.empty()
            df = pd.DataFrame(st.session_state.data)
            st.dataframe(df)
            break
        else:
            with placeholder.form(key=str(num)):
                new_student = NewStudent(page_id=num)

                if st.form_submit_button('register'):
                    st.session_state.data.append({
                        'id': num, 'name': new_student.name, 'age': new_student.age})
                    st.session_state.num += 1
                    placeholder.empty()
                    placeholder2.empty()
                else:
                    st.stop()

main()
