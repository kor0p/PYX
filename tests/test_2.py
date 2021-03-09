from pyx import cached_tag, state, button, style, br, div

@cached_tag.update(title='div')
def func(tag):
    tag.count = state(0)
    def increment():
        tag.count += 1
    def decrement():
        tag.count -= 1
    return [
        div(_class='text', children=f'Count: {tag.count}'),
        br(),
        button(_class='button', on_click=increment, children="++"),
        br(),
        button(_class='button', on_click=decrement, children="––"),
        style(scoped=True, children='''
            .text, .button {
                font-size: 1rem;
            }
            .button {
                background: none;
                border: 1px solid red;
                border-radius: .1rem;
            }
        ''')
    ]


# can be simplified as __pyx__ = func
def __pyx__():
    """entrypoint for pyx"""
    return func()
