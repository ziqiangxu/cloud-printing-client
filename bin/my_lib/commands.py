import os
import bin.settings as settings

def kill_all_threading():
    os.system("tskill %s" % settings.PROJECT_NAME)