// lab — 독립 공간 전용 스크립트. 외부 의존성 없음.
(function () {
  'use strict';

  var stamp = document.getElementById('stamp');
  if (!stamp) return;

  var now = new Date();
  var pad = function (n) { return String(n).padStart(2, '0'); };

  stamp.textContent =
    now.getFullYear() + '-' + pad(now.getMonth() + 1) + '-' + pad(now.getDate()) +
    ' ' + pad(now.getHours()) + ':' + pad(now.getMinutes());
})();
