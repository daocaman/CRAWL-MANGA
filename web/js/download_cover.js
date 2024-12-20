function downloadCover(event) {
    event.preventDefault();
    
    const link = document.getElementById('link').value;
    const numberCovers = parseInt(document.getElementById('numberCovers').value);

    document.getElementById("loadingScreen").classList.remove("d-none");
    eel.download_cover(link, numberCovers);
}
