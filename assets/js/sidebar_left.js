window.addEventListener('resize', function(){
    var icons =document.getElementsByTagName('svg');
    for(let i = 0; i < icons.length;i++)
    {
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

window.onbeforeunload = function(e){
    var icons =document.getElementsByTagName('svg');
    for(let i = 0; i < icons.length;i++)
    {
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
}
// la-width : 1024 , md-width : 768