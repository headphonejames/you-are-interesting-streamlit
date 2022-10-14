import streamlit as st
import lib.util as util
import constants.pages as pages

# init current page state
current_page_key = util.get_session_state_value(st, pages.CURRENT_PAGE, initValue=pages.ENRTY)
pages.map[current_page_key].execute()