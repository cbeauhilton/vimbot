document.addEventListener("DOMContentLoaded", function () {
  const textareas = document.querySelectorAll("textarea");
  textareas.forEach(function (textarea) {
    textarea.addEventListener("keydown", function (event) {
      if (event.ctrlKey && event.key === "Enter") {
        event.preventDefault();
        const form = textarea.closest("form");
        if (form) {
          form.dispatchEvent(new Event("submit"));
        }
      }
    });
  });
});
