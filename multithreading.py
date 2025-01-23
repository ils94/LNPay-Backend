import threading


def run_in_thread(target_func, *args, **kwargs):
    """
    Executes a given function in a separate thread.

    :param target_func: The function to run in a thread.
    :param args: Positional arguments to pass to the target function.
    :param kwargs: Keyword arguments to pass to the target function.
    :return: The Thread object.
    """
    thread = threading.Thread(target=target_func, args=args, kwargs=kwargs)
    thread.start()
    return thread
