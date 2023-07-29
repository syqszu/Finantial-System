const dropZone = document.querySelector('#bottom-left-input-area');

dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
});

dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    // 处理拖放的文件
});
