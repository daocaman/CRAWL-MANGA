function resizeImages(event) {
    event.preventDefault();

    const isHorizontal = document.getElementById('isHorizontal').checked;
    const isMultiple = document.getElementById('isMultiple').checked;
    const targetFolder = document.getElementById('targetFolder').value;

    document.getElementById('loadingScreen').classList.remove('d-none');
    eel.resize_images(targetFolder, isMultiple, isHorizontal);
}