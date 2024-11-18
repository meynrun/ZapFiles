window.addEventListener("beforeunload", function (e) {
    eel.handle_exit()
});

document.addEventListener("DOMContentLoaded", () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            } else {
                entry.target.classList.remove("show");
            }
        });
    });

    const hiddenElements = document.getElementsByClassName("hidden");
    Array.from(hiddenElements).forEach((el) => observer.observe(el));
});