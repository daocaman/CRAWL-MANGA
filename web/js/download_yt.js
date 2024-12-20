function downloadYt(event) {
    event.preventDefault();
    
    yt_link = document.getElementById("link").value;
    yt_type = document.getElementById("format").value;
    file_yt = document.getElementById("fileYt").value;
    is_playlist = document.getElementById("isPlaylist").checked ? 2 : 1;
    is_convert = document.getElementById("isConvert").checked;
    quality = document.getElementById("quality").value;

    document.getElementById("loadingScreen").classList.remove("d-none");
    eel.download_yt(yt_link, yt_type, is_playlist, file_yt, quality, is_convert);

}

