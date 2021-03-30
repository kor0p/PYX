from pyx import cached_tag, state, button, style, br, div


@cached_tag.update(title='div')
def func(tag):
    tag.count = state(0)

    def increment():
        tag.count += 1

    def decrement():
        tag.count -= 1

    if tag.count > 0:
        color = 'green'
    elif tag.count < 0:
        color = 'red'
    else:
        color = 'black'

    return [
        div(_class='text', children=f'Count: {tag.count}'),
        br(),
        button(_class='button', on_click=increment, children="+ +"),
        button(_class='button', on_click=decrement, children="– –"),
        style(
            scoped=True,
            lang='sass',
            children=f'''
            *
                font-size: 2rem
                margin: 0.1rem
            .text
                color: {color}
            .button
                background: none
                border: .1rem solid red
                border-radius: .1rem
                
                &:focus, &:hover
                    border-color: green
                    background: aliceblue''',
        ),
    ]


# can be simplified as __pyx__ = func
def __pyx__():
    """entrypoint for pyx"""
    return func()
