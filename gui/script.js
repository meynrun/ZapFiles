window.addEventListener("beforeunload", () => {
    eel.handle_exit()
});

window.addEventListener("resize", () => {
    if (window.outerWidth < 400){
        window.resizeTo(400, window.outerHeight);
    }
    else if (window.outerHeight < 500){
        window.resizeTo(window.outerWidth, 500);
    }
})

document.addEventListener("DOMContentLoaded", () => {
    const pages = document.querySelector(".pages").children;

    pages[0].classList.add("show");
    document.querySelector("#port").value = "8888";
});


function change_page(targetPage) {
    const pages = document.querySelector(".pages").children;

    // Найти текущую страницу
    const currentPage = Array.from(pages).find(page =>
        page.classList.contains("show")
    );

    if (currentPage) {
        currentPage.classList.remove("show");
        currentPage.classList.add("hidden");
    }

    // Показать новую страницу
    const target = Array.from(pages).find(page =>
        page.id === targetPage
    );

    if (target) {
        target.classList.remove("hidden");
        target.classList.add("show");
    }
}