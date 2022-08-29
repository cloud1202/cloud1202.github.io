---
layout: post
title: Html JS(javascript) 적용하는 방법
tags: html jekyll githubpage javascript
toc: true
date: 2022-08-19 16:05 +0900
category: Html
---

사실 **JS**를 잘 알지 못한다. 대학교 커리큘럼에 포함되어있어서 몇번 다뤄보았고, 현재에는 Jekyll 블로그를 만드느라 다루는 것이 전부여서 전문적인 지식이 아닌 기록의 용도로 가끔 참고하기 위해 포스팅 합니다.  

거두절미하고 본론으로 들어갔습니답

## Html에서 JS 사용하기
웹을 조금이라도 다뤄본 사람이라면 모를수가 없는 웹 기본 지식 3가지가 있는 것 같다.(본인 기준)  
웹의 기본 뼈대는 **HTML**, 그 위에 특색에 맞게 살을 입히는 **CSS**, 여러 동작을 구현하게 해주는 **JS**  
이 세가지만 있다면 뭐든 다 만들수 있다. 라고 생각한다.  

**JS**는 사용하는 방법이 두 가지가 있다.
1. `.html` 확장자 파일에 `<script>` 태그에 포함시켜 사용하는 방법
2. `.js` 확장자 파일을 따로 만들어 `<script>` 태그에 포함시켜 사용하는 방법

사실 두 방법은 개발자의 기준에서 다른 것이지 컴퓨터의 입장에서 볼때는 **똑같다**
단지, `.js` 확장자 파일을 따로 만드는 경우가 사람입장에서 관리하기가 편해 따로 만들어 사용하고 있을 뿐이다.(본인 기준)  

## .html 확장자 파일에 포함시키는 방법
`.html` 확장자 파일에 포함시키는 방법은 간단하다. `<script>` 태그에 구현할 **JS** 코드를 넣어주기만 하면 된다.
```html
<script>
    function testFunction()
    {
        console.log("Hello, World!");
    }
</script>
```
위의 방식으로 코드를 넣어줬다면 **Console** 창에서 `Hello, World!` 문구를 볼 수 있을 것이다.
코드를 넣는 위치는 사실 상관 없다고 보고 있으며,**(본인 기준)** 대부분의 경우 `<head>` 태그안에 넣어주는 것이 일반적이다.  

### 웹에서 Console 창 보는 법
웹에서의 Console창은 `F12` 키를 누르면 볼 수 있다.
![ConsoleView](/assets/img/2022-08-19-JavaScript-import/Console.PNG "ConsoleView")

붉은 네모박스 안에 표시된 것들은 웹에서 바로 볼 수 있는 개발툴 같은 것이다.  
이것을 설명하는 것은 해당 포스트의 주제와 어긋나 자세히는 설명하지 않을 예정이다.

## .js 확장자 파일에 포함시키는 방법
`.js` 확장자 파일에 포함시키는 방법은 `.html` 파일에 포함시키는 방법과 거의 유사하다. `<script>` 태그안의 코드를 따로 분리한 경우라고 보면 될 것 같다.

```html

<script src="/경로/myscript.js" type="text/javascript"></script>

```

```javascript
function testFunction()
    {
        console.log("Hello, World!");
    }
```
