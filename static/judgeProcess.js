document.getElementById('config-button').addEventListener('click', function() {
            fetch('/get_file_info')
                .then(response => response.json())
                .then(data => {
                    const fileNames = data.file_names;
                    if (fileNames.length === 2) {
                        console.log('Received 2 files');
                        console.log('File names:', fileNames);
                        // 进行进一步的判断逻辑
                    } else if (fileNames.length === 3) {
                        console.log('Received 3 files');
                        console.log('File names:', fileNames);
                        // 进行进一步的判断逻辑
                    }
                });
        });