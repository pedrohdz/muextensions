from docutils.parsers.rst import directives
from decorator import decorator


def preserve_docutils_directives(func):
    def wrapper(func, *args, **kwargs):
        # pylint: disable=protected-access
        original = directives._directives
        directives._directives = original.copy()
        result = func(*args, **kwargs)
        directives._directives = original
        return result
    return decorator(wrapper, func)
