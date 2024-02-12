/* ******************************************************
   * main.ts: Typescript functionality for landing.html *
   * https://git.krischerven.info/dev/portfolio-webpage *
   ****************************************************** */

function set_code_tab(name: String) {
  for (const lang of ["welcome", "metaprog", "search-for-users", "website", "chatbot"]) {
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
    const hour = eval("dayjs().hour()")
    console.assert(typeof (hour) === 'number', "dayjs().hour() did not return a number")
    return hour
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

function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function toggle_AI_assistant_dialogue() {
  const element = document.getElementById("AI-assistant")!!
  if (getComputedStyle(element).display === "none") {
    element.classList.remove("fade-out")
    element.style.display = "block"
  } else {
    element.classList.add("fade-out")
    await sleep(300)
    element.style.display = "none"
  }
}

function ask_chatbot_question_interactively(question: string) {
  const host = location.host.startsWith("localhost") ?
    "http://localhost:5000" : "https://krischerven.info"
  fetch(host + "/question/" + question)
    .then((response) => response.json())
    .then((json) => console.log(json.response))
    .catch((error) => console.error(error))
}

function ask_chatbot_question() {
  const host = location.host.startsWith("localhost") ?
    "http://localhost:5000" : "https://krischerven.info"
  const input = document.getElementById("AI-message-input") as HTMLInputElement
  const question = input.value
  input.value = ""
  // /question/ without an argument is 404
  if (question === "") {
    create_chatbot_question("")
    create_chatbot_answer("Please ask me a question.", 2)
  } else {
    create_chatbot_question(question)
    fetch(host + "/question/" + question)
      .then((response) => response.json())
      .then((json) => create_chatbot_answer(json.response))
      .catch((error) => console.error(error))
  }
}

function create_chatbot_question(question: string) {
  const span = document.createElement("span")
  span.innerText = "Q: " + question
  const messageArea = document.getElementById("AI-message-area")!!
  messageArea.appendChild(span)
  messageArea.appendChild(document.createElement("br"))
}

function create_chatbot_answer(answer: string, br=1) {
  const span = document.createElement("span")
  span.innerText = (answer == "") ? "An error occured on the server." : "A: " + answer
  const messageArea = document.getElementById("AI-message-area")!!
  messageArea.appendChild(span)
  for (let i = 0; i < br; i++)
    messageArea.appendChild(document.createElement("br"))
  console.log("CHATBOT: " + answer)
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