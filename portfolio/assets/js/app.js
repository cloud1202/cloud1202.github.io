/* 포트폴리오 동작 — 의존성 없음.
   JS가 없어도 그리드와 게시물은 정적 HTML로 전부 보인다.
   여기서 하는 일은 (1) 초과 카드 접기 (2) 이미지 확대뿐이다. */
(function () {
  'use strict';

  // 이 클래스가 붙은 뒤에만 CSS가 초과 카드를 숨긴다.
  document.documentElement.classList.add('js');

  // 1) Show more
  document.querySelectorAll('.category .more').forEach(function (button) {
    button.addEventListener('click', function () {
      var section = button.closest('.category');
      if (section) section.classList.add('is-open');
    });
  });

  // 2) 이미지 확대
  var zoomable = Array.prototype.slice.call(document.querySelectorAll('.shot img[data-zoom]'));
  if (!zoomable.length) return;

  var overlay = null;
  var picture = null;
  var current = 0;

  function show(index) {
    current = (index + zoomable.length) % zoomable.length;
    var source = zoomable[current];
    picture.src = source.getAttribute('data-zoom');
    picture.alt = source.alt || '';
  }

  function close() {
    if (!overlay) return;
    overlay.remove();
    overlay = null;
    document.body.classList.remove('lb-open');
    document.removeEventListener('keydown', onKey);
    zoomable[current].focus({ preventScroll: true });
  }

  function onKey(event) {
    if (event.key === 'Escape') close();
    else if (event.key === 'ArrowRight') show(current + 1);
    else if (event.key === 'ArrowLeft') show(current - 1);
  }

  function open(index) {
    overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');

    picture = document.createElement('img');
    overlay.appendChild(picture);

    [['lb-close', '✕', close],
     ['lb-prev', '‹', function () { show(current - 1); }],
     ['lb-next', '›', function () { show(current + 1); }]
    ].forEach(function (spec) {
      var button = document.createElement('button');
      button.type = 'button';
      button.className = spec[0];
      button.textContent = spec[1];
      button.addEventListener('click', function (event) {
        event.stopPropagation();
        spec[2]();
      });
      overlay.appendChild(button);
    });

    overlay.addEventListener('click', close);
    document.body.appendChild(overlay);
    document.body.classList.add('lb-open');
    document.addEventListener('keydown', onKey);
    show(index);
  }

  zoomable.forEach(function (image, index) {
    image.tabIndex = 0;
    image.addEventListener('click', function () { open(index); });
    image.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        open(index);
      }
    });
  });
})();
