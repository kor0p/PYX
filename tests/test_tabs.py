from pyx import tabs, tab, style
from flask import request

import tests.test_1 as test_1
import tests.test_2 as test_2
import tests.test_3 as test_3


def main():
    tabs_list = [
        dict(name='page 1', children=test_1.__pyx__(), url='/?page=1'),
        dict(name='page 2', children=test_2.__pyx__(), url='/?page=2'),
        dict(name='page 3', children=test_3.__pyx__(), url='/?page=3')
    ]
    return [
        tabs(
            _class='content',
            children=[tab(**kw) for kw in tabs_list]
        ),
        style(scoped=True, children='''
            ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #f1f1f1;
            }
            
            /* Float the list items side by side */
            tab {
                float: left;
            }
            
            /* Change background color of links on hover */
            tabs tab:hover {
                background-color: #ddd;
            }
            
            /* Create an active/current tablink class */
            tabs tab:focus, tabs tab[active] li {
                background-color: #ccc;
            }
            
            /* Style the links inside the list items */
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
            
            /* Style the tab content */
            .content {
                padding: 6px 12px;
                -webkit-animation: fadeEffect 1s;
                animation: fadeEffect 1s;
            }
        '''),
    ]


__pyx__ = main
