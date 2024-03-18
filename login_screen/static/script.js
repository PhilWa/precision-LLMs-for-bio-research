function step() {
    fetch("/next", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            updateGrid(data);
        })
        .catch((error) => {
            console.error("Error fetching next generation:", error);
        });
}
setInterval(step, 100);
