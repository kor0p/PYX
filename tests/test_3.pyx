from pyx import Tag, state, select, p  # not necessary, really

@cached_tag.update(title='div')
def func(tag):
    tag.selected = state(1)
    items = {0: 'first', 1: 'second', 2: 'third'}
    def _select(value):
        tag.selected = int(value)
    return <>
        <p>Key: {tag.selected}</p>
        <style src='/pyx/static/css/pyx.css'/>
        <p @click.right:prevent={lambda: 'GOT IT'}>Value: {items[tag.selected]}</p>
        <select
            items={items}
            @change:prevent={_select}
            value={tag.selected}
        />
    </>


__pyx__ = func
