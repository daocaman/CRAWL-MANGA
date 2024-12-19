function createMetadata(event) {
  event.preventDefault();
  let targetFolder = document.getElementById("targetFolder").value;
  let comicInfoFile = document.getElementById("comicInfoFile").value;
  let bookmarkFile = document.getElementById("bookmarkFile").value;
  let isMultipleFolder = document.getElementById("isMultipleFolder").checked;

  document.getElementById("loadingScreen").classList.remove("d-none");
  eel.create_metadata(
    bookmarkFile == "" ? null : bookmarkFile,
    comicInfoFile == "" ? null : comicInfoFile,
    targetFolder == "" ? null : targetFolder,
    isMultipleFolder
  );
}
