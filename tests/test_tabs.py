from pyx import tabs, tab, style

import tests.test_1 as test_1
import tests.test_2 as test_2
import tests.test_3 as test_3


def main():
    test_1_content = test_1.__pyx__()
    test_2_content = test_2.__pyx__()
    test_3_content = test_3.__pyx__()
    return [
        tabs(children=[
            tab(name='page 1', children=test_1_content),
            tab(name='page 2', children=test_2_content),
            tab(name='page 3', children=test_3_content),
        ]),
        style(scoped=True, children='''// TODO: add styles'''),
    ]


__pyx__ = main
