function OnClickDropdown(dropdown, index){
    // state 0 = up, 1 = down
    const imoji_down_arrow = "&#x1F53D";
    const imoji_up_arrow = "&#x1F53C";

  if (dropdown.getAttribute('state') == 1)
    {
      dropdown.innerHTML = dropdown.getAttribute('name') + " " + imoji_down_arrow;
    dropdown.setAttribute('state', '0');
    }
    else
    {
      dropdown.innerHTML = dropdown.getAttribute('name') + " " + imoji_up_arrow;
      dropdown.setAttribute('state', '1');
  }
  $("#dropdown-item-" + index).slideToggle("fast");
}

function OnClickSocialIcon(url){
  localStorage.removeItem('search_text');
  document.location.href = url;
}