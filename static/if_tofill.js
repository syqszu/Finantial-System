function if_tofill(){
alert("关键数据为空，请按照‘填充指引表’填充后重启程序");
fetch('/if_tofill', {     method: 'POST' })
            .then(response => response.text())
            .then(data => {
                console.log(data)
            });
}
