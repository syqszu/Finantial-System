 function setOutputPath() {
            var path = document.getElementById("output-filepath").value;
            fetch('/set_output_path', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ path: path }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('路径已设置:', data.path);
            })
            .catch(error => {
                console.error('设置路径时出现错误:', error);
            });
        }