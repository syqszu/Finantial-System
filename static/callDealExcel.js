 function callDealExcel() {
                    fetch('/run_deal_excel')
                        .then(response => response.text())
                        .then(data => alert(data))
                        .catch(error => console.error(error));
                }