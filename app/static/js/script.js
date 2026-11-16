function setupDescriptionToggles(button) {
    const descriptions = document.querySelectorAll(".project-description");

    descriptions.forEach(description => {
        const button = description.nextElementSibling;

        // Temporarily remove the line limit to measure the full description.
        description.classList.add("expanded");

        const fullHeight = description.scrollHeight;

        // Restore the collapsed state.
        description.classList.remove("expanded");

        const collapsedHeight = description.clientHeight;
        
        // Only show the button if the description was actually clipped
        button.hidden = fullHeight <= collapsedHeight + 1;
    });
}

function toggleDescription(button) {
    const description = button.previousElementSibling;

    description.classList.toggle("expanded");

    button.textContent = description.classList.contains("expanded")
        ? "Read less"
        : "Read more";
}

document.addEventListener("DOMContentLoaded", setupDescriptionToggles);