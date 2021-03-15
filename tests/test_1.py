from pyx import Tag

@Tag
def name(*_, attr):
    return 'Child'

def __pyx__():
    """entrypoint for pyx"""
    return name(attr=1, only_view_attr=True)
