document.addEventListener("DOMContentLoaded", function () {
  const darkModeEmoji = document.getElementById("darkModeEmoji");
  const body = document.body;

  const darkModePreference = localStorage.getItem("darkMode");
  if (darkModePreference === "true") {
    body.classList.add("dark");
    darkModeEmoji.textContent = "🌙";
  }

  darkModeEmoji.addEventListener("click", function () {
    if (body.classList.contains("dark")) {
      body.classList.remove("dark");
      darkModeEmoji.textContent = "☀️";
      localStorage.setItem("darkMode", "false");
    } else {
      body.classList.add("dark");
      darkModeEmoji.textContent = "🌙";
      localStorage.setItem("darkMode", "true");
    }
  });

  const queryTextarea = document.getElementById("query");
  const defaultQueries = [
    "How do I work up anemia?",
    "What are the diagnostic criteria for sepsis?",
    "How do I manage acute pancreatitis?",
    "What are the indications for dialysis in acute kidney injury?",
    "I'm the intern on Brittingham. When should I show up?",
    "When does the VU cafeteria close?",
  ];

  // Set a random default query as the placeholder
  const randomQuery =
    defaultQueries[Math.floor(Math.random() * defaultQueries.length)];
  queryTextarea.setAttribute("placeholder", randomQuery);

  // Clear the textarea when the user starts typing
  queryTextarea.addEventListener("input", function () {
    if (this.value === "") {
      this.setAttribute("placeholder", randomQuery);
    } else {
      this.removeAttribute("placeholder");
    }
  });

  async function copyToClipboard() {
    const responseContent = document.getElementById("response-content");
    const text = responseContent.innerText;

    try {
      await navigator.clipboard.writeText(text);
      alert("Response copied to clipboard!");
    } catch (err) {
      console.error("Failed to copy response: ", err);
    }
  }
});
