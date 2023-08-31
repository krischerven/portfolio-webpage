/* * ***************************************************** *
   * debug.ts: Developer debug tools for portfolio-webpage *
   * ***************************************************** * */

function codeFontSize(className="") : string {
  if (className !== "")
    className = "."+className
  return getComputedStyle(document.querySelector("div.codearea pre code"+className)!!).fontSize
}

function codeSize(codeClassName="") : Array<any> {
  return [codeFontSize(codeClassName), screen.width]
}