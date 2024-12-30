function reformatManga(event) {
    event.preventDefault();
    
    const targetFolder = document.getElementById('targetFolder').value;
    const isMultiple = document.getElementById('multipleFolders').checked;
    const isDelete = document.getElementById('deleteFolders').checked;

    document.getElementById('loadingScreen').classList.remove('d-none');
    eel.reformat_manga(targetFolder, isMultiple, isDelete);
}