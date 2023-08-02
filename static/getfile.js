const fileInput1 = document.querySelector('#jinxiang-filepath');
const fileInput2 = document.querySelector('#xiaoxiang-filepath')

// const fileInputs = {fileInput1, fileInput2};

// for (let i = 0; i < 2; i++) {
    fileInput1.addEventListener('change', () => {
        let file = fileInput1.files[0];
        let formData = new FormData();
        formData.append('file', file);
        fetch('/getfile', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
            .then(data => console.log(data))
            .catch(error => console.error(error));
    });
// }

 fileInput2.addEventListener('change', () => {
        let file = fileInput2.files[0];
        let formData = new FormData();
        formData.append('file', file);
        fetch('/getfile', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
            .then(data => console.log(data))
            .catch(error => console.error(error));
    });