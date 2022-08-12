function OnClickDropdown(dropdown){
    // state 0 = up, 1 = down
    const imoji_down_arrow = "&#x1F53D";
    const imoji_up_arrow = "&#x1F53C";

    console.log(dropdown.getAttribute(dropdown.getAttribute('name') + " " + imoji_down_arrow));
    if(true)
    {
    }
    else
    {
        dropdown.innerHTML = dropdown.getAttribute('name') + " " + imoji_up_arrow;
    }
}