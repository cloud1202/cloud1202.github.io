function EnterKeyPress(baseURL)
{
  if(window.event.keyCode == 13)
  {
    OnClickSearchButton(baseURL);
  }
}

function OnClickSearchButton(baseURL)
{
  var searchText = document.getElementById('search-text').value;

  if(searchText === "" || searchText === null || searchText.trim().length === 0)
  {
    alert("검색어를 입력해주세요.");
    postReset();
    document.getElementById('search-text').value = '';
    localStorage.removeItem('search_text');
    return;
  }
    
  if(baseURL != document.location.href)
  {
    localStorage.setItem('search_text', searchText);
    document.location.href = baseURL;
    return;
  }

  searchPost(searchText);
}

function searchPost(searchText)
{
  var data = document.getElementsByClassName("post-title");

  var searchTexts = searchText.split(' ');

  for(let i = 0; i < searchTexts.length; i++)
  {
    for(let j = 0; j < data.length; j++)
    {
      var regex = new RegExp(searchText[i], "i");
  
      if(regex.test(data[j].innerText) == false)
      {
        data[j].parentNode.style.display = 'none';
      }
      else
      {
        data[j].parentNode.style.display = '';
      }
    }
  }
}

function postReset()
{
  var data = document.getElementsByClassName("post-entry");

  for(let i = 0; i < data.length; i++)
  {
    data[i].style.display = '';
  }
}