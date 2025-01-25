document.addEventListener("DOMContentLoaded", ()=>{

    const optionList = document.querySelector('.option-list');
    const tableDiv = document.querySelector('#root-div-2-table');
    const scorersDiv = document.querySelector('#root-div-2-scorers');
    const nMatchesDiv = document.querySelector('#root-div-2-next-matches');
    const pMatchesDiv = document.querySelector('#root-div-2-previous-matches');
    const arr = {
        "0":tableDiv,
        "1":scorersDiv,
        "2":nMatchesDiv,
        "3":pMatchesDiv
    }
    optionList.addEventListener('change', (choice) => {
        for (let i in arr){
            
            if(i == choice.target.value){
                arr[i].style.display = "block"
            }else{
                arr[i].style.display = "none"
            }
            
        }
    })
    

})