'use strict';
(function(){
  function localtimeize(el) {
    const ms = parseInt(el.getAttribute('data-utc-ms'));
    const serverTime = el.innerText;
    el.innerText = new Date(ms).toLocaleString();
    el.setAttribute('data-utc-converted', 'yes');
    el.setAttribute('title', `${serverTime} server time`)
  }
  window.addEventListener('load', () => {
    document.querySelectorAll('span[data-utc-ms]').forEach(localtimeize);
  });
})();
