from pagez import *

#page constants
CURRENT_PAGE = "currentpage"
ENRTY = "entry"
START_SHIFT = "start-shift"
FINISH_SHIFT = "finish-shift"
PROMPTS = "prompts"
WORKERS = "workers"
WAITING_FOR_FRIEND = "waiting-for-friend"
CONNECTION_BEGINS = "connection-begins"
CONNECTION_SELECT_PROMPT = "connection-select-prompt"
CONNECTION_HAPPENING = "connection-happening"
CONNECTION_COMPLETE = "connection-complete"

map = {
    ENRTY: page_entry,
    WORKERS: page_manage_worker_list,
    PROMPTS: page_prompts,
    START_SHIFT: page_select_current_worker,
    FINISH_SHIFT: page_shift_finished,
    WAITING_FOR_FRIEND: page_waiting_for_friend,
    CONNECTION_BEGINS: page_connection_begins,
    CONNECTION_SELECT_PROMPT: page_connection_select_prompt,
    CONNECTION_HAPPENING: page_connection_happening,
    CONNECTION_COMPLETE: page_connection_completed
}
