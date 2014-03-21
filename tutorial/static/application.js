var onload_function = function() {             
    var head  = document.getElementsByTagName('head')[0]
    var util_script = document.createElement('script')
    util_script.type= 'text/javascript'
    util_script.src = '/clientlib/utils.js'
    util_script.onload = function() {
        ld_util.onload({}, '/tutorial/application.html', null)
    }
    head.appendChild(util_script)
}

window.addEventListener('DOMContentLoaded', onload_function, false)