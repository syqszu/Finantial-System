const dragAreas = document.querySelectorAll('.drag-excel');
const mergeButton = document.querySelector('#merge-button');
const progressBar = document.querySelector('#progress-bar');
const progressText = document.querySelector('#progress-text');
const progressArea = document.querySelector('#progress-area');

dragAreas.forEach(dragArea => {
    dragArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dragArea.classList.add('active');
    });

    dragArea.addEventListener('dragleave', () => {
        dragArea.classList.remove('active');
    });

    dragArea.addEventListener('drop', (e) => {
        e.preventDefault();
        let file = e.dataTransfer.files[0];
        let formData = new FormData();
        formData.append('file', file);
        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
            .then(data => {
                console.log(data);
                dragArea.classList.add("success");
                let text = dragArea.querySelector('.up-drag-excel h3');
                text.textContent = '上传成功';
            })
            .catch(error => console.error(error));
        dragArea.classList.remove('active');
    });
});

mergeButton.addEventListener('click', () => {
    dragAreas.forEach(dragArea => {
        dragArea.classList.remove('success');
        let texts = dragArea.querySelectorAll('.up-drag-excel h3');
        texts[0].textContent = '本月进项文件/';
        texts[1].textContent = '匹配临时完成表';
    });
    progressArea.style.display='flex';
    progressBar.classList.add('active');
    setTimeout(() => {
        progressBar.classList.remove('active');
        progressText.textContent = "合并成功";
    }, 10000);
});
