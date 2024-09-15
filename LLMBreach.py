import db_handler
import module_handler

def startup():
    print("LLMBreach is starting up...")
    db_handler.pull_from_db()
    module_handler.verify_module()

