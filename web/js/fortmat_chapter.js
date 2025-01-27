function load_f_e_images() {
  eel.load_f_e_images()((chapters) => {
    document.getElementById("loadingScreen").classList.remove("d-none");
    const form = document.getElementById("formatForm");
    form.innerHTML = "";
    chapters.forEach((chapter) => {
      form.innerHTML += `
          <div class="row my-2 mx-1 py-2 border rounded-2">
            <div class="col-2">
              <p>${chapter.title}</p>
            </div>
            <div class="col-3">
              <label for="${chapter.title}_${chapter.start_page}">
                <img class="review_image" src="Chapters/${chapter.title}/${chapter.start_page}" alt="${chapter.title}" />
              </label>
              <input type="checkbox" id="${chapter.title}_${chapter.start_page}" name="chapter_id" />
              </div>
            <div class="col-3">
              <label for="${chapter.title}_${chapter.end_page}">
                <img class="review_image" src="Chapters/${chapter.title}/${chapter.end_page}" alt="${chapter.title}" />
              </label>
              <input type="checkbox" id="${chapter.title}_${chapter.end_page}" name="chapter_id" />
            </div>
          </div>
        `;
    });
    document.getElementById("loadingScreen").classList.add("d-none");
  });
}

function format_chapter() {
  let formFormat = document.getElementById("formatForm");
  const selectedChapters = Array.from(
    formFormat.querySelectorAll('input[name="chapter_id"]:checked')
  ).map((checkbox) => checkbox.id);

  document.getElementById("loadingScreen").classList.remove("d-none");
  eel.format_chapter(selectedChapters);
}
