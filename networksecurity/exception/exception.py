import sys
class NetworkSecurityException(Exception):
    def _init__(self, error_details, error_message:sys):
        self.error_message= error_message
        _,_,exec_tb = error_details.exec_info()
        
        self.lineno = exec_tb.tb_lineno
        self.file_name = exec_tb.tb_frame.f_code.co_filename
        
    def __str__(self) -> str:
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))    

if __name__ == "__main__":
    try:
        a = 1/0
        print("This will not be printed",a)
    except Exception as e:
        raise NetworkSecurityException(e,sys)    