# Surasith Boonaneksap Aug 7th, 2021
from typing import Any
from re import Pattern, fullmatch

def _arg_handling(input: Any,
                  expected_type: Any = None, 
                  expected_value: Any = None, 
                  err_msg: str = None) -> None:
    """
    Check if a value/variable is of certain type and value.

    An exception is raised if the type or the value is not correct.
    This function only support an int, float, str, and dict{str: str}.
    The expected value can be exact, a range for numeric types using 
    a list (inclusive), or a regular expression for string 
    using re.Pattern.
    
    Parameters
    ----------
    input: Any
        A value or variable of the supported types
    expected_type: Any, default = None
        Expected input's type [int, float, str, dict]
    expected_value: Any, optional
        The expected value of input. If not specified, No value is checked.
    err_msg: str, optional
        The error message for an exception if an input is not correct.
        
    Raises
    ------
    ValueError
        Raise when the input doesn't have the expected value or the 
        parameters doesn't have the correct value.
    TypeError
        Raise when the input doesn't have the expected type or the 
        parameters doesn't have the correct type.

    Notes
    -----
    The key and value of dict must be string. A list of two regexes 
    can be used. The first one for the keys and the second for the values.

    Examples
    --------
    >>> import re
    >>> _arg_handling(5, int, 5)
    >>> _arg_handling([1,2,3], list, [1,2,3])
    Traceback (most recent call last):
        ...
    TypeError: list is not supported
    >>> _arg_handling(1, int, [0,6])
    >>> _arg_handling("email@email.com", str, re.compile(".+@.+"))
    >>> _arg_handling({"a":"A","b":"B"}, dict, \
    ... [re.compile("."), re.compile(".")])
    """

    supported_types = [int, float, str, dict]
    supported_expected_value_types = [*supported_types, list, Pattern]
    numeric = [int, float]
    
    #Exception: An int can be converted to float
    if (type(input) == int and expected_type == float):
        input = float(input)

    # The arguments' types must be supported
    if (type(input) not in supported_types):
        raise TypeError(f"{str(type(input))[8:-2]} is not supported")
    
    if (expected_type not in supported_types):
        raise TypeError("The provided expected type is not supported")
    
    if (type(err_msg) not in [str, type(None)]):
        print(type(err_msg))
        raise TypeError("The error message must be a string")
    
    # Check if the input's type matched the expected type
    if (type(input) != expected_type):
        raise TypeError(err_msg if err_msg else
                        f"Expected an input of type "
                        f"{str(expected_type)[8:-2]}")
    # Check the expected value if given
    elif expected_value:
        #Check the type of the expected value
        if (type(expected_value) not in supported_expected_value_types):
            raise TypeError(f"The type of the expected value is invalid")
        
        if (type(expected_value) in supported_types 
                and type(expected_value) != type(input)):
            raise TypeError("For an exact value comparison, the type of "
                            "the input and expected value must be the same")
        
        if (type(expected_value) == Pattern and type(input) != str):
            raise TypeError("A regular expression can only be used with "
                            "a string input")
            
        if (type(expected_value) == list 
                and type(input) not in [int, float, dict]):
            raise TypeError("A list can only be used with an int, a float, "
                            "or a dict")
        
        # Exact comparison
        elif (type(input) == type(expected_value)
                and input != expected_value):
            raise ValueError(err_msg if err_msg else
                                f"Expected an input's value: "
                                f"{expected_value}")
            
        # Regular Expression for string
        elif (type(input) == str and type(expected_value) == Pattern):
            if fullmatch(expected_value, input) == None:
                raise ValueError(err_msg if err_msg else
                                    f"No matching pattern found")
        
        # Range for int, float, and dict
        elif (type(expected_value) == list):
            if (len(expected_value) != 2):
                raise ValueError(f"The expected value must "
                                 f"have a list of size 2")
            else:
                if (type(input) == dict):
                    
                    for i in expected_value:
                        if type(i) != Pattern:
                            raise ValueError("The key and value must "
                                             "be pattern")
                            
                    for key in input:
                        if type(key) != str or type(input[key]) != str:
                            raise TypeError(err_msg if err_msg else \
                                "Keys and values must be string")
                        
                        if (fullmatch(expected_value[0], key) == None 
                                or fullmatch(expected_value[1], input[key])\
                                    == None):
                            raise ValueError(err_msg if err_msg else \
                                "Unexpected key or value")
                    
                elif (type(input) in [int, float]):
                    
                    for i in expected_value:
                        if type(i) not in [int, float]:
                            raise ValueError("The range of the expected "
                                             "values must be numeric")
                    
                    expected_value = sorted(expected_value)
                    
                    if (input < expected_value[0] 
                            or input > expected_value[1]):
                        raise ValueError(err_msg if err_msg else "Unexpected value")
                    
                else:
                    raise TypeError("list expected value is incompatible "
                                    "with a string input")