/* * ***************************************************** *
   * utils.ts: Utility functions for portfolio-webpage *
   * ***************************************************** * */

function pxToEm (px, element) {
  element = element === null || element === undefined ? document.documentElement : element;
  let e = document.createElement('div');
  e.style.setProperty('position', 'absolute', 'important');
  e.style.setProperty('visibility', 'hidden', 'important');
  e.style.setProperty('font-size', '1em', 'important');
  element.appendChild(e);
  let baseFontSize = parseFloat(getComputedStyle(e).fontSize);
  e.parentNode!!.removeChild(e);
  return px / baseFontSize;
}