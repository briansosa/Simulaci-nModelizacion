class Validator:

    @classmethod
    def IsNumeric(cls, number):
        isPostiveInteger = number.isdigit()
        isNegativeInteger =  number.startswith("-") and number[1:].isdigit()
        return isPostiveInteger or isNegativeInteger        
