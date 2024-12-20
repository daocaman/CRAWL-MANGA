function renameFiles(event) {
    event.preventDefault();

    const targetFolder = document.getElementById('targetFolder').value;
    const startIndex = document.getElementById('startIndex').value;
    const sortFiles = document.getElementById('sortFiles').checked;

    document.getElementById('loadingScreen').classList.remove('d-none');
    eel.rename_files(targetFolder, sortFiles, startIndex);
}