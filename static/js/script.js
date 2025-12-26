function updateDateTime() {
    const now = new Date();
    document.getElementById("datetime").innerText =
        now.toLocaleDateString() + " " + now.toLocaleTimeString();
}

setInterval(updateDateTime, 1000);
updateDateTime();

let page = window.currentPage || 1;
let loading = false;

const content = document.querySelector(".content");

content.addEventListener("scroll", () => {
    console.log("content scrolling...");

    if (loading) return;

    if (content.scrollTop + content.clientHeight >= content.scrollHeight - 200) {
        loading = true;
        page++;

        const loadingEl = document.getElementById("loading");
        if (loadingEl) loadingEl.style.display = "block";

        fetch(`/?page=${page}`)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const newItems = doc.querySelectorAll(".inventory-card");

                if (newItems.length === 0) {
                    if (loadingEl) loadingEl.innerText = "No more products";
                    return;
                }

                const grid = document.getElementById("inventoryGrid");
                newItems.forEach(item => grid.appendChild(item));

                loading = false;
                if (loadingEl) loadingEl.style.display = "none";
            });
    }
});
