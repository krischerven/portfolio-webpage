/* # ################################################### #
   # main.ts: Typescript functionality for landing.html. #
   # ################################################### # */

function set_code_tab(name: String) {
  for (const lang of ["welcome", "metaprog", "website", "typescript", "rust"]) {
    const x = document.getElementById(`${lang}-tab`)
    if (x != null)
      x.style.display = "none"
    document.getElementById(`${lang}-tab-content`)!!.style.display = "none"
  }
  const x = document.getElementById(`${name}-tab`)
  if (x != null)
      x.style.display = ""
  document.getElementById(`${name}-tab-content`)!!.style.display = ""
}
