import streamlit as st
import lib.util as util
import constants

# init current page state
current_page_key = util.get_session_state_value(st, constants.CURRENT_PAGE, initValue=constants.ENRTY)
constants.map[current_page_key].execute()