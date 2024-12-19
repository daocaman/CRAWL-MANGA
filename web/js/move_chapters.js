function moveChapters(event) {
  event.preventDefault();
  console.log("move_chapters");
  let folChaptersFile = document.getElementById("folChaptersFile").value;
  let mangaTitle = document.getElementById("mangaTitle").value;
  let deleteAfterMove = document.getElementById("deleteAfterMove").checked;

  console.log(folChaptersFile, mangaTitle, deleteAfterMove);

  document.getElementById("loadingScreen").classList.remove("d-none");
  eel.move_chapters(folChaptersFile, mangaTitle, deleteAfterMove);
}
