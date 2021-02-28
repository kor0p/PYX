from pyx import render, run_app, __APP__

from tests import test_1, test_2, test_3


@__APP__.route('/1')
def test_1_route():
    return render(test_1.__pyx__())


@__APP__.route('/2')
def test_2_route():
    return render(test_2.__pyx__())


@__APP__.route('/3')
def test_3_route():
    return render(test_3.__pyx__())


if __name__ == '__main__':
    run_app()
else:
    app = __APP__  # for vercel
