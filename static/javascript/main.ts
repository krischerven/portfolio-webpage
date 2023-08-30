/* * ************************************************** *
   * main.ts: Typescript functionality for landing.html *
   * https://git.krischerven.info/dev/portfolio-webpage *
   * ************************************************** * */

function set_code_tab(name: String) {
  for (const lang of ["welcome", "metaprog", "website"]) {
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

const Dayjs = () => {
  function hour(): number {
    return eval("dayjs().hour()")
  }
  return { hour: hour }
}

function get_welcome_blurb(hour_?: number): string {
  const hour: number = hour_ ?? Dayjs().hour()
  if (hour > 2 && hour < 12)
    return "Good morning."
  else if (hour >= 12 && hour < 18)
    return "Good afternoon."
  else
    return "Good evening."
}

function set_welcome_blurb() {
  document.getElementById("welcome-blurb")!!.innerHTML = get_welcome_blurb()
}

if (typeof document === 'undefined')
  describe('main.ts', function () {
    const chai = require('chai')
    it('test_welcome_blurb', function () {
      function log2(i: number, x: string): number {
        //console.log(i, "(" + x + ")")
        return i
      }
      for (let i = 0; i < 3; i++)
        chai.expect(get_welcome_blurb(log2(i, "evening"))).equal("Good evening.")
      for (let i = 3; i < 12; i++)
        chai.expect(get_welcome_blurb(log2(i, "morning"))).equal("Good morning.")
      for (let i = 12; i < 18; i++)
        chai.expect(get_welcome_blurb(log2(i, "afternoon"))).equal("Good afternoon.")
      for (let i = 18; i < 24; i++)
        chai.expect(get_welcome_blurb(log2(i, "evening"))).equal("Good evening.")
    });
  });

if (typeof document !== 'undefined')
  set_welcome_blurb()