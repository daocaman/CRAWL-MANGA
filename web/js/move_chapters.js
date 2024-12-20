function moveChapters(event) {
  event.preventDefault();

  let folChaptersFile = document.getElementById("folChaptersFile").value;
  let mangaTitle = document.getElementById("mangaTitle").value;
  let deleteAfterMove = document.getElementById("deleteAfterMove").checked;

  document.getElementById("loadingScreen").classList.remove("d-none");
  eel.move_chapters(folChaptersFile, mangaTitle, deleteAfterMove);
}
