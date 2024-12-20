function archive_manga(event) {
  event.preventDefault();
  
  target_folder = document.getElementById("targetFolder").value;
  multiple_folders = document.getElementById("multipleFolders").checked;
  delete_folders = document.getElementById("deleteFolders").checked;

  document.getElementById("loadingScreen").classList.remove("d-none");
  eel.archive_manga(target_folder, multiple_folders, delete_folders);
}
