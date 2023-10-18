def static_variable(default_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not hasattr(wrapper, "static_variable"):
                wrapper.static_variable = default_value
            return func(*args, **kwargs)
        return wrapper
    return decorator


@static_variable(0)  # Initialize the static variable to a default value
def my_function():
    my_function.static_variable += 1
    print("Static variable:", my_function.static_variable)


# Test the function
my_function()
my_function()
my_function()
