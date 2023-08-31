"use strict";
function codeFontSize(className = "") {
    if (className !== "")
        className = "." + className;
    return getComputedStyle(document.querySelector("div.codearea pre code" + className)).fontSize;
}
function codeSize(codeClassName = "") {
    return [codeFontSize(codeClassName), screen.width];
}
