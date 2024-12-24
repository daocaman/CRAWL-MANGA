function convertTs(event) {
  event.preventDefault();

  folder_ts = document.getElementById("folderTs").value;
  eel.convert_ts(folder_ts);
}