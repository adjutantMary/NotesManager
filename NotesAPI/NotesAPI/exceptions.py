from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    """
    The `core_exception_handler` function in Python handles exceptions by calling specific handlers
    based on the exception class.

    :param exc: The `exc` parameter in the `core_exception_handler` function refers to the exception
    that was raised in the code. It contains information about the exception such as the type of
    exception, error message, and traceback details
    :param context: The `context` parameter typically refers to the execution context or environment in
    which the code is running. It can include information about the current state of the program,
    variables, and other relevant data that can be used to handle exceptions or errors. In the provided
    code snippet, the `context` parameter is
    :return: The `core_exception_handler` function returns the response after handling any specific
    exceptions using the `_handle_generic_error` function if the exception class matches
    'ValidationError'. Otherwise, it returns the original response.
    """
    response = exception_handler(exc, context)
    handlers = {"ValidationError": _handle_generic_error}

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response.data = {"errors": response.data}

    return response
