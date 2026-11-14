function toggleDescription(button) {
    const description = button.previousElementSibling;

    description.classList.toggle("expanded");

    if (description.classList.contains("expanded")) {
        button.textContent = "Read less";
    } else {
        button.textContent = "Read more";
    }
}