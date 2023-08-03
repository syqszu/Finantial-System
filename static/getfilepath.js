// 获得进项、销项、输出文件路径
document.getElementById("config-button").addEventListener("click", function() {
    var jinxiangFilepath = document.getElementById("jinxiang-filepath").value;
    var xiaoxiangFilepath = document.getElementById("xiaoxiang-filepath").value;
    var outputFilepath = document.getElementById("output-filepath").value;
    console.log("jinxiangFilepath",jinxiangFilepath);
    console.log("xiaoxiangFilepath",xiaoxiangFilepath);
    console.log("outputFilepath",outputFilepath);
});