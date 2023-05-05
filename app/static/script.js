function showContent(button) {
    dropdownContent = button.nextElementSibling;
    dropdownContent.classList.toggle('show');
}

window.onclick = (event) => {
    if (!event.target.matches('.dropdown')) {
        const dropdownContent = document.querySelector('.dropdown-content');
        if (dropdownContent) {
            if (dropdownContent.classList.contains('show')) {
                dropdownContent.classList.remove('show');
            }
        }
    }
}