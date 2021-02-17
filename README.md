# PYX
### A python-based realtime frontend framework

# use
```python
# tests/test_1.py
from pyx import Tag

@Tag
def name(*, attr):
    return 'Child'

def __pyx__():
    """entrypoint for pyx"""
    return name(attr=1)
```
will render
```html
...
<body>
    <pyx>
        <name attr="1">
            Child
        </name>
    </pyx>
</body>
...
```
### and
```python
# tests/test_2.py
from pyx import cached_tag, button, state

@cached_tag.update(name='div')
def func(tag):
    tag.count = state(0)
    def increment():
        tag.count += 1
    return button(on_click=increment, children="++")

# can be simplified as __pyx__ = func
def __pyx__():
    """entrypoint for pyx"""
    return func()
```
will render
```html
...
<body>
    <pyx>
        <div>
            <button title="++" on_click="<fn hash>"/>
        </div>
    </pyx>
</body>
...
```
## with parser .pyx
```python
# tests/test_3.pyx
from pyx import Tag, state, select, p  # not necessary, really

@cached_tag.update(name='div')
def func(tag):
    tag.selected = state(1)
    items = {0: 'first', 1: 'second', 2: 'third'}
    def _select(value):
        tag.selected = int(value)
    return <>
        <p>Key: {tag.selected}</p>
        <p @click.right:prevent={lambda: 'GOT IT'}>Value: {items[tag.selected]}</p>
        <select
            items={items}
            @change:prevent={_select}
            value={tag.selected}
        />
    </>


__pyx__ = func
```
will render
```html
...
<body>
    <div>
        <p>Key: 0</p>
        <!-- will be called on contextmenu event with .preventDefault() -->
        <p @click.right:prevent="<fn hash>">Value: first</p>
        <!-- will be called on change event with .preventDefault() -->
        <select @change:prevent="<fn hash>" value="0">
            <option label="first" value="0" selected>first</option>
            <option label="second" value="1">second</option>
            <option label="third" value="2">third</option>
        </select>
    </div>
</body>
...
```
### `__PYX__=modulename python -m pyx.app`

# install
### now PYX use Flask for render
- `pip install -r requirements.txt`

# .pyx
## File watcher for Intellij Idea family:
### Editor -> File Types -> New -> .pyx
### Settings -> Tools -> File Watchers -> New ->
#### File type: .pyx
#### Program: python
#### Arguments: <project path>/pyx/pyx_parser.py
### #TODO: cli file watcher && other IDE support

