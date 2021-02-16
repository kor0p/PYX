from pyx import cached_tag, state, button, br

@cached_tag.update(name='div')
def func(tag):
    tag.count = state(0)
    def increment():
        tag.count += 1
    return [
        'Count: ', tag.count, br(),
        button(on_click=increment, children="++"),
    ]


# can be simplified as __pyx__ = func
def __pyx__():
    """entrypoint for pyx"""
    return func()
