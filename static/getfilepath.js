// 获得输出文件路径
document.getElementById("config-button").addEventListener("click", function() {

    var outputFilepath = document.getElementById("output-filepath").value;

    console.log("outputFilepath",outputFilepath);

    fetch('/getfilepath', {
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

