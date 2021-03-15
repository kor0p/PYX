from pyx import render, run_app, __APP__

from tests import test_1, test_2, test_3, test_tabs


@__APP__.get('/1')
def test_1_route():
    return render(test_1)


@__APP__.get('/2')
def test_2_route():
    return render(test_2)


@__APP__.get('/3')
def test_3_route():
    return render(test_3)


@__APP__.get('/tabs')
def test_tabs_route():
    return render(test_tabs)


if __name__ == '__main__':
    run_app(name='tests.app_fastapi')
else:
    app = __APP__  # for uvicorn / vercel
