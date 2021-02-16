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
### `__PYX__=modulename python pyx/app.py`

# install
- `pip install -r requirements.txt`

# run
- `__PYX__=file.py python pyx app.py`


# .pyx
## File watcher for Intellij Idea family:
### Editor -> File Types -> New -> .pyx
### Settings -> Tools -> File Watchers -> New ->
#### File type: .pyx
#### Program: python
#### Arguments: <project path>/pyx/pyx_parser.py

