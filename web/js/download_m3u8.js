function downloadM3u8(event) {
  event.preventDefault();

  file_m3u8 = document.getElementById("fileM3u8").value;
  eel.download_m3u8(file_m3u8);
}