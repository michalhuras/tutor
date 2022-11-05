""" Module contains base class for singleton classes to inherit from. """


class SingletonMeta(type):
    """ Implementation of the Singleton base class. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """ Class instance is being returned. If it wasn't created yet, it is going to be created. """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
