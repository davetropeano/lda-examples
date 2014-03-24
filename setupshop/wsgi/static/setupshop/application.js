SUS = 'http://setupshop.me/ns#'
BG = 'http://ibm.com/ce/blog/ns#'

var onload_function = function() {
    var prefixes = {}
        prefixes[SUS] = 'sus'
        prefixes[BG] = 'bg'

    var type_to_theme_map = {}
        type_to_theme_map[SUS+'OnlineStore'] = '/setupshop/shop/sus_shop.html'
        type_to_theme_map[SUS+'Category'] = '/setupshop/shop/sus_shop.html'
        type_to_theme_map[SUS+'Product'] = '/setupshop/shop/sus_shop.html'
        type_to_theme_map[SUS+'BackOffice'] = '/setupshop/sell/sus_sell.html'
        type_to_theme_map[BG+'BlogService'] = '/setupshop/blog/sus_blog.html'
        type_to_theme_map[BG+'Blog'] = '/setupshop/blog/sus_blog.html'
        type_to_theme_map[BG+'BlogPost'] = '/setupshop/blog/sus_blog.html'

    var head  = document.getElementsByTagName('head')[0]
    var util_script = document.createElement('script')
    util_script.type= 'text/javascript'
    util_script.src = '/sitedesign/utils.js'
    util_script.onload = function() {ld_util.onload(prefixes, type_to_theme_map)}
    head.appendChild(util_script)
}

window.addEventListener('DOMContentLoaded', onload_function, false)
