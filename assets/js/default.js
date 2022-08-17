// sidebar-left social icon size change
// la-width : 1024 , md-width : 768
window.onload = function(e){
    var icons =document.getElementsByTagName('svg');
    for(let i = 0; i < icons.length;i++)
    {
        if(icons[i].parentElement.classList.contains('social-icon') == false)
        {
            continue;
        }

        if(window.matchMedia('(max-width: 768px)').matches)
        {
            icons[i].classList.remove('fa-2x');
            icons[i].classList.remove('fa-sm');
            icons[i].classList.remove('fa-xs');
            icons[i].classList.remove('fa-lg');
            icons[i].classList.add('fa-lg');
        }
        else if(window.matchMedia('(min-width: 768px) and (max-width: 1441px)').matches)
        {
            icons[i].classList.remove('fa-2x');
            icons[i].classList.remove('fa-sm');
            icons[i].classList.remove('fa-xs');
            icons[i].classList.remove('fa-lg');
        }
        else if(window.matchMedia('(min-width: 1441px)').matches)
        {
            icons[i].classList.remove('fa-2x');
            icons[i].classList.remove('fa-sm');
            icons[i].classList.remove('fa-xs');
            icons[i].classList.remove('fa-lg');
            icons[i].classList.add('fa-lg');
        }
    }
    var body = document.body,
        html = document.documentElement;

    var height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
    document.getElementById("sidebar-left").style.height = height+"px";
    document.getElementById("sidebar-right").style.height = height+"px";
    
}

window.onbeforeunload = function(e){
    
    var body = document.body,
        html = document.documentElement;

    var height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
    document.getElementById("sidebar-left").style.height = height+"px";
    document.getElementById("sidebar-right").style.height = height+"px";
}

window.addEventListener('resize', function(){
    var icons =document.getElementsByTagName('svg');
    for(let i = 0; i < icons.length;i++)
    {
        if(icons[i].parentElement.classList.contains('social-icon') == false)
        {
            continue;
        }
        if(window.matchMedia('(max-width: 768px)').matches)
        {
            icons[i].classList.remove('fa-2x');
            icons[i].classList.remove('fa-sm');
            icons[i].classList.remove('fa-xs');
            icons[i].classList.remove('fa-lg');
            icons[i].classList.add('fa-lg');
        }
        else if(window.matchMedia('(min-width: 768px) and (max-width: 1441px)').matches)
        {
            icons[i].classList.remove('fa-2x');
            icons[i].classList.remove('fa-sm');
            icons[i].classList.remove('fa-xs');
            icons[i].classList.remove('fa-lg');
        }
        else if(window.matchMedia('(min-width: 1441px)').matches)
        {
            icons[i].classList.remove('fa-2x');
            icons[i].classList.remove('fa-sm');
            icons[i].classList.remove('fa-xs');
            icons[i].classList.remove('fa-lg');
            icons[i].classList.add('fa-lg');
        }
    }
}, true);