'use strict';
(function(){

  /****************************************************************
   * Convert datetimes to local time on ALL pages.
   ****************************************************************/

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

  /****************************************************************
   * "Wrap long lines" on the paste detail pages
   ****************************************************************/

  /* If anybody can get https://codepen.io/winny-/pen/BaKJYqd working I can
     delete this javascript! */
  window.addEventListener('load', () => {
    const p = document.querySelector('#body-container pre');
    if (!p) return;
    document.getElementById('toggle-wrap').addEventListener('click', ({ target }) => {
      if (target.checked) p.classList.add('word-wrap');
      else p.classList.remove('word-wrap');
    });
  });

  /****************************************************************
   * Convert datetimes between local time and UTC for the custom
   * expiry entry on the "Make a paste" page.
   ****************************************************************/

  window.addEventListener('load', () => {
    const customExpiryDate = document.getElementById('id_custom_expiry_date');
    const customExpiryTime = document.getElementById('id_custom_expiry_time');
    if (customExpiryDate === null || customExpiryTime === null) return;

    /**
     * Convert from server time (UTC) to localtime by
     * 1. summing the date and time as milliseconds,
     * 2. Get the seconds since the local time's midnight.
     * 3. Compute the date seconds without the local time seconds since midnight.
     * 4. Set the  date and time inputs
     */
    function initialize() {
      const dn = customExpiryDate.valueAsNumber;
      const tn = customExpiryTime.valueAsNumber;
      if (isNaN(dn) || isNaN(tn)) return null;
      const dt = new Date(dn + tn);
      const secondsSinceMidnight = dt.getSeconds()+60*dt.getMinutes()+60*60*dt.getHours();
      const dateWithoutTime = dt.valueOf() - secondsSinceMidnight;
      const msSinceMidnight = 1000*secondsSinceMidnight;
      customExpiryDate.valueAsNumber = dateWithoutTime;
      customExpiryTime.valueAsNumber = msSinceMidnight;
    }

    initialize();

    let fixed = false;

    function submit(ev) {
      if (fixed) return;
      fixed = true;
      const mlookup = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12};
      const dn = customExpiryDate.valueAsNumber;
      const tn = customExpiryTime.valueAsNumber;
      const dtl = new Date(dn+tn);
      if (isNaN(dn) || isNaN(tn)) return null;
      const [_, plusminus, hrs, mins] = new Date().toString().match(/GMT(?:([-+])(\d{2})(\d{2}))?/);
      const offset2 = 60*(parseInt(hrs)*60 + parseInt(mins)) * ((plusminus === '-') ? -1 : +1);
      const dt = new Date(dtl.valueOf() - offset2*1000);
      const [__, ___, d, mo, y, h, m, s] = dt.toUTCString().match(/(([0-9]{1,2}) ([A-Z][a-z]+) (\d{4}) (\d{2}):(\d{2}):(\d{2}))/);
      const moNum = mlookup[mo].toString();
      const dv = `${y.padStart(4, "0")}-${moNum.padStart(2, "0")}-${d.padStart(2, "0")}`;
      const tv = `${h.padStart(2, "0")}:${m.padStart(2, "0")}:${s.padStart(2, "0")}`;
      customExpiryDate.value = dv;
      customExpiryTime.value = tv;
    }

    window.addEventListener('submit', submit);
    window.addEventListener('unload', submit);
  });

})();
