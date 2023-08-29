/* * ***************************************************** *
   * debug.ts: Developer debug tools for portfolio-webpage *
   * ***************************************************** * */

function codeFontSize() {
  return getComputedStyle(document.querySelector("div.codearea pre code")!!).fontSize
}