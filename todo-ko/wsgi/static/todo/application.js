BP = 'http://open-services.net/ns/basicProfile#'
TD = 'http://example.org/todo#'

var onload_function = function() {
    var type_to_theme_map = {}
    type_to_theme_map[BP+'Container'] = '/todo/list.html'
    type_to_theme_map[TD+'Item'] = '/todo/item.html'

    var head  = document.getElementsByTagName('head')[0]
    var util_script = document.createElement('script')
    util_script.type= 'text/javascript'
    util_script.src = '/clientlib/utils.js'
    
    util_script.onload = function() {
        ld_util.onload({}, type_to_theme_map, null)
    }
    head.appendChild(util_script)
}

window.addEventListener('DOMContentLoaded', onload_function, false)