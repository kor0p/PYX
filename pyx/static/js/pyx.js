window.ALL = () => $('*')
window.__DOM__ = {
    error: "error>*",
}

function unifyModifiers(str) {
    /**  in: on_click__right___prevent
     *   out: @click:right.prevent
     */
    return str
        .replace(/^on_/, '@')
        .replace(/___/g, '.')
        .replace(/__/g, ':')
}


function getModifiers(str) {
    /**  in:  @click:right.prevent    or    on_click__right___prevent
     *   out: ['@click', ':right', '.prevent']
     */
    return unifyModifiers(str).split(/(?=[:.])/g)
}

function getRegExpModifiers(event) {
    /**  event: name of event to get regex modifiers
     *   ex:             @click:right.prevent       on_click__right___prevent             */
    return new RegExp(`((@${event}([:.][^\\W_]+)*)|(on_${event}(_{2,3}[^\\W_]+)*))$`, 'i')
}

$.fn.event = function(pattern) {
    const res = []
    this.each(
        (idx, tag) => {
            const attrs = Object.values(tag.attributes)
                .filter(v => pattern.test(v.name))
                .map(attr => ({
                    tag,
                    attr,
                    modifiers: getModifiers(attr.name),
                    name: attr.name,
                    value: attr.value,
                }))
            if (attrs.length) {
                res.push(...attrs)
            }
        }
    )
    return res
}

$.fn.regex = function(pattern, fn, args){
    fn = fn || $.fn.text
    return this.filter(function() {
        console.log(arguments)
        return pattern.test(fn.apply(this, args))
    })
}

$.fn.withAttr = function(pattern) {
    return this.regex(pattern, function () {
        return Object.values(this.attributes)
            .map(v => v.name).join(',')
    })
}

window.printRequestError = function printRequestError(params) {
    $(window.__DOM__.error).replaceWith(params
        ? `ERROR:\n  kwargs: ${JSON.stringify(params)}`
        : ''
    )
}

window.getPyxId = function getPyxId (el) {
    const _id = el.length && el[0].__self_id__
    if (_id) {
        return _id
    } else {
        return el.attr('pyx-id')
    }
}

window.findPyxParent = function findPyxParent (el) {
    let parent = el.parent()
    if (Object.is(parent[0], document)) {
        return el
    }
    while (parent) {
        if (getPyxId(parent)) {
            return parent
        }
        el = el.parent()
        parent = parent.parent()
    }
}

window.makeId = function makeId () {
    $('[pyx-id]').toArray().reverse().map(t => {
        const e = $(t)
        const parent = findPyxParent(e)
        t.__parent__ = parent[0]
        t.__self_id__ = getPyxId(e)
        t.__id__ = getPyxId(parent)
        e.removeAttr('pyx-id')
        if (e.attr('pyx-dom') === '') {
            e.removeAttr('pyx-dom')
            window.__DOM__[t.__self_id__] = t
            window.__DOM__[t.__id__] = t.__parent__
        }
    })
}

window.__request = async function __request(event_type, el, url, params) {
    params.id = el.__id__
    try {
        window.printRequestError() // clear error
        const res = await fetch(
            `pyx/${el.tagName.toLowerCase()}___${event_type}___${url}?` + $.param(params),
        )
        if (res.status !== 200) {
            console.log(await res.text())
            return window.printRequestError(params)
        }
        try {
            const {
                target,
                html,
            } = await res.json()
            $(window.__DOM__[target]).replaceWith(html)
            window.init()
            console.log(html)
        } catch (e) {
            console.log(e)
        }
    } catch (e) {
        console.log(e)
        window.printRequestError(params)
    }
}


window.__event_actions__ = {
    prevent (event) {
        try {
            event.preventDefault()
            return true
        } catch (e) {
            return false
        }
    }
}


window.__event_details__ = {
    click: {
        left: e => e.left,
        right: e => e.right,
        middle: e => e.middle,
    },
}

function checkModifiers(el, event) {
    if (el.modifiers.length > 1) {
        let [name, ...modifiers] = el.modifiers
        name = name.slice(1)
        for (const m of modifiers) {
            if (m[0] === ':') {
                const actionFn = window.__event_actions__[m.slice(1)]
                if (!actionFn) continue
                if (!actionFn(event)) {
                    // if callback return false, stop event
                    return
                }
            } else if (m[0] === '.') {
                const checkFn = window.__event_details__[name]?.[m.slice(1)]
                if (!checkFn) continue
                if (!checkFn(event)) {
                    // if callback return false, stop event
                    return
                }
            } else {
                throw new Error('Unknown event modifier')
            }
        }
    }
    return true
}


window.__events__ = {
    change (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { value: el.tag.value })
    },
    click (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, {})
    },
    mouseover (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
    mouseout (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
    keydown (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
    keyup (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
    keypress (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
    load (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
    submit (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
    custom (el, event) {
        if (!checkModifiers(el, event)) return
        return window.__request(el.name, el.tag, el.value, { m: el.modifiers.join(',') })
    },
}

window.makeEvents = async function makeEvents() {
    for await (const [name, loader] of Object.entries(window.__events__)) {
        console.log(name)
        for await (const el of ALL().event(getRegExpModifiers(name))) {
            const self = $(el.tag)
            console.log(self, name, loader, el)
            self.off(name).on(name, async function (event) {
                return await loader.call(self, el, event)
            })
        }
    }
}

window.init = function init() {
    window.makeId()
    window.makeEvents()
}


$(document).ready(function () {
    window.init()
})
