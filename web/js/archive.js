function archive_manga(event) {
  event.preventDefault();
  // console.log("archive");
  target_folder = document.getElementById("targetFolder").value;
  multiple_folders = document.getElementById("multipleFolders").checked;
  delete_folders = document.getElementById("deleteFolders").checked;

  eel.archive_manga(target_folder, multiple_folders, delete_folders);
}