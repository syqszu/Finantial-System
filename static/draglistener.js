class FileUploader {
    constructor({
                    element,
                    uploadUrl,
                }) {
        if (element instanceof HTMLElement) {
            this.element = element;
        } else {
            throw new Error('element is not an HTMLElement')
        }
        this.uploadUrl = uploadUrl;
        this.#init();
    }

    // public props
    tasks = [];

    // private methods
    #init = () => {
        const dropAreaDOM = this.element.querySelector('.drag-excel');
        dropAreaDOM.addEventListener('drop', this.#handleDrop);
        dropAreaDOM.addEventListener('dragover', this.#handleDragover);
    }
    //
    // #listenToEvents = () => {
    //     const dropAreaDOM = this.element.querySelector('.area');
    //     dropAreaDOM.addEventListener('drop', this.#handleDrop);
    //     dropAreaDOM.addEventListener('dragover', this.#handleDragover);
    // }

    #handleDrop = (e) => {
        // Prevent file from being opened
        e.preventDefault();

        if (e.dataTransfer.items) {
            // Use DataTransferItemList interface to access files
            for (const item of e.dataTransfer.items) {
                if (item.kind === 'file') {
                    const file = item.getAsFile();
                    console.log('file: ', file);
                    alert("上传成功");
                    // this.#upload(file);
                }
            }
        } else {
            // Use DataTransfer interface to access the files
            for (const file of e.dataTransfer.files) {
                console.log('file: ', file);
                // this.#upload(file);
            }
        }
    }

    #handleDragover = (e) => {
        // Prevent file from being opened
        e.preventDefault();
    }
}