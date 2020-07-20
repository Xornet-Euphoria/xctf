"""
    Under Construcion
"""


from enum import Enum, auto


class FailureError(Exception):
    pass


class Result():
    self.__err_msg = "fail..."


    def __init__(self, res, val):
        self.__res = res
        self.__value = val

    
    def isSuccess(self):
        return self.__res == SuccessOrFailure.SUCCESS


    def unwrap(self, expect_success=True, failure_value=None):
        if self.isSuccess():
            return self.__value

        if not expect_success:
            return failure_value

        self.raiseErr()


    def stop(self, log=True):
        if not self.isSuccess():
            if log:
                print(self.__err_msg)
            exit()


    def raiseErr(self, log=True):
        if not self.isSuccess():
            if log:
                print(self.__err_msg)
            raise FailureError


class SuccessOrFailure(Enum):
    SUCCESS = auto(),
    FAILURE = auto()