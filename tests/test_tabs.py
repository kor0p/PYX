from pyx import tabs, div, tab, style, __APP__ as app
from pyx.utils.app import utils

from tests import test_1, test_2, test_3


def main():
    query = utils.current.query
    tabs_list = [
        dict(name='page 1', children=test_1.__pyx__, url='/?page=1'),
        dict(name='page 2', children=test_2.__pyx__, url='/?page=2'),
        dict(name='page 3', children=test_3.__pyx__, url='/?page=3'),
    ]
    return div(
        [
            tabs(
                selected='page ' + query['page'] if 'page' in query else None,
                _class='content',
                children=[tab(**kw) for kw in tabs_list],
            ),
            style(
                scoped=True,
                head=True,
                lang='scss',
                children='''
                    tabs {
                        ul {
                            list-style-type: none;
                            margin: 0;
                            padding: 0;
                            overflow: hidden;
                            background-color: #f1f1f1;
                        }
                        .content {
                            padding: 6px 12px;
                            -webkit-animation: fadeEffect 1s;
                            animation: fadeEffect 1s;
                        }
                        tab {
                            float: left;

                            &:hover {
                                background-color: #ddd;
                            }
                            &:focus, &[active] li {
                                background-color: #ccc;
                            }

                            li {
                                font-family: "Lato", sans-serif;
                                display: inline-block;
                                color: black;
                                text-align: center;
                                padding: 14px 16px;
                                text-decoration: none;
                                transition: 0.3s;
                                font-size: 17px;
                            }
                        }
                    }''',
            ),
        ]
    )


__pyx__ = main
