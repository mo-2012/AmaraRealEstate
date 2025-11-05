document.addEventListener("DOMContentLoaded", () => {
    const propertyType = document.getElementById("propertyType");
    const fields = {
        area: document.querySelector('input[name="area"]'),
        rooms: document.querySelector('input[name="rooms"]'),
        baths: document.querySelector('input[name="baths"]'),
        priceFrom: document.querySelector('input[name="priceFrom"]'),
        priceTo: document.querySelector('input[name="priceTo"]')
    };

    propertyType.addEventListener("change", () => {
        Object.values(fields).forEach(f => f.classList.add("hidden"));
        const value = propertyType.value;
        if (["شقة", "بيت", "فيلا"].includes(value)) {
            fields.area.classList.remove("hidden");
            fields.rooms.classList.remove("hidden");
            fields.baths.classList.remove("hidden");
            fields.priceFrom.classList.remove("hidden");
            fields.priceTo.classList.remove("hidden");
        } else if (["أرض مباني", "أرض صناعية"].includes(value)) {
            fields.area.classList.remove("hidden");
            fields.priceFrom.classList.remove("hidden");
            fields.priceTo.classList.remove("hidden");
        }
    });

    const imageUpload = document.getElementById("imageUpload");
    const fileInput = document.getElementById("fileInput");
    const imagePreview = document.getElementById("imagePreview");

    imageUpload.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => handleFiles(e.target.files));

    imageUpload.addEventListener("dragover", (e) => {
        e.preventDefault();
        imageUpload.style.borderColor = "#fff";
    });
    imageUpload.addEventListener("dragleave", (e) => {
        e.preventDefault();
        imageUpload.style.borderColor = "#7b5cff";
    });
    imageUpload.addEventListener("drop", (e) => {
        e.preventDefault();
        imageUpload.style.borderColor = "#7b5cff";
        handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
        imagePreview.innerHTML = "";
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement("img");
                img.src = e.target.result;
                imagePreview.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }
});
