document.getElementById("merge-button").addEventListener("click", function() {

    fetch('/merge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
         body: JSON.stringify({
             outputFilepath: outputFilepath
        })
    })
    .then(response => response.text())
    .then(data => {
        // 处理从后台返回的数据
        console.log(data);
    })
    .catch(error => {
        // 处理错误
        console.error(error);
    });

});