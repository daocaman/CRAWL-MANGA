function downloadManga(event) {
    // eel.download_manga();
    event.preventDefault(); // Prevent form submission

    // console.log("Form data:", formData);
    ele = document.getElementById("mangaUrl");

    link = document.getElementById("link").value;
    server = document.getElementById("server").value;
    startChapterIndex = parseInt(document.getElementById("startChapterIndex").value);
    numChapters = parseInt(document.getElementById("numChapters").value);

    document.getElementById("loadingScreen").classList.remove("d-none");

    eel.download_manga(link, numChapters, server, startChapterIndex);

}