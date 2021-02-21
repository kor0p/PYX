from pyx import render, run_app, __APP__

import test_1
import test_2
import test_3


@__APP__.route('/1')
def test_1_route():
    return render(test_1.__pyx__())


@__APP__.route('/2')
def test_2_route():
    return render(test_2.__pyx__())


@__APP__.route('/3')
def test_3_route():
    return render(test_3.__pyx__())


run_app()
