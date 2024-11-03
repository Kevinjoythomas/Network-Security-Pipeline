import sys
from networkSecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _, _, exc_tb  = error_details.exc_info()
        
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.filename
        
    def __str__(self):
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )
        
try:
    logger.logging.info("Enter the try block")
    a = 1/0
    # Some code that might cause an exception
except NetworkSecurityException as e:
    raise NetworkSecurityException(e, sys)