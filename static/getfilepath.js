// 获得进项、销项、输出文件路径
document.getElementById("config-button").addEventListener("click", function() {

    var jinxiangFilepath = document.getElementById("jinxiang-filepath").value;
    var xiaoxiangFilepath = document.getElementById("xiaoxiang-filepath").value;
    var outputFilepath = document.getElementById("output-filepath").value;

    console.log("jinxiangFilepath",jinxiangFilepath);
    console.log("xiaoxiangFilepath",xiaoxiangFilepath);
    console.log("outputFilepath",outputFilepath);

    fetch('/getfilepath', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
         body: JSON.stringify({
            jinxiangFilepath: jinxiangFilepath,
            xiaoxiangFilepath: xiaoxiangFilepath,
             outputFilepath: outputFilepath
        })
    })
    .then(response => response.json())
    .then(data => {
        // 处理从后台返回的数据
        console.log(data);
    })
    .catch(error => {
        // 处理错误
        console.error(error);
    });

});

