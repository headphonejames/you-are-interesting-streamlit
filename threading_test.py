from streamlit.ReportThread import add_report_ctx

# Your thread creation code:
thread = threading.Thread(target=runInThread, args=(onExit, PopenArgs))
add_report_ctx(thread)
thread.start()


job_thread = PopenCall(onExit, PopenArgs)
job_thread.join()  # this will block until the thread exits

def PopenCall(onExit, PopenArgs):
    def runInThread(onExit, PopenArgs):
        script_ID = PopenArgs[1]
        proc = subprocess.Popen(PopenArgs)
        proc.wait()
        onExit(script_ID)
        return

    thread = threading.Thread(target=runInThread, args=(onExit, PopenArgs))
    thread.start()

    return thread

def onExit(script_ID):
    st.write("Done processing", script_ID + ".")

PopenArgs = [
    "python", os.path.join("src", "models" , fn),
    json_path, cycle_name
]
print ("Running {} in background.......".format(PopenArgs))
PopenCall(onExit, PopenArgs)