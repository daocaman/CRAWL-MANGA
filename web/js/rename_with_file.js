function createFileList() {
    const targetFolder = document.getElementById("targetFolder").value;

    document.getElementById('loadingScreen').classList.remove('d-none');
    eel.create_file_list(targetFolder);
}

function renameFiles() {
    document.getElementById('loadingScreen').classList.remove('d-none');
    eel.rename_files_with_file();
}
