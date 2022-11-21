
import sys

def error_message_details(error,error_details:sys):
    _,_,exec_info = error_details.exc_info()
    file = exec_info.tb_frame.f_code.co_filename
    error_message = "Error occurred in file [{0}] line number [{1}] error message  [{2}]".format(
        file, exec_info.tb_lineno, str(error))
    return error_message


class CustomException(Exception):

    def __init__(self, error_message,error_details:sys) -> None:
        super().__init__(error_message)

        self.error_message = error_message_details (error_message,error_details=error_details)

    def __str__(self) -> str:
        return self.error_message