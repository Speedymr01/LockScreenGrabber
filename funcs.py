def ini_log(Log_name):
    import logging
    logging.basicConfig(filename = Log_name, level=logging.INFO)
    logging.info('Log sucsessfully initiated')

def log_fini():
    import logging
    logging.info('Script Finished')
def enter_to_fini():
    fini = input('PRESS ENTER TO EXIT')

