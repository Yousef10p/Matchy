


document.addEventListener('DOMContentLoaded', ()=>{
  const comp = document.querySelectorAll('.list-group-item')
  const keysOFLG = document.querySelectorAll('.hidden')
    comp.forEach(c=>{
        keysOFLG.forEach(key => {
            
            
            if(key.textContent === c.id){
                c.style.cursor = 'pointer';
                c.onmouseover = ()=>{
                    c.classList.add('bg-warning')
                    c.classList.remove('text-light')
                    c.classList.add('text-dark')
                }
                c.onmouseout = ()=>{
                    c.classList.remove('bg-warning')
                    c.classList.remove('text-dark')
                    c.classList.add('text-light')
                }
                c.onclick =  ()=> {
                    const link = c.getAttribute('data-link'); 
                    window.location.href = link;
                }
            }
        })
                
    })
    const icon = document.querySelector('.icon img')
    icon.style.cursor = 'pointer';
    icon.onclick = ()=>{
        const link = icon.getAttribute('data-link'); 
        window.open(link, '_blank');
    }
    
   


    const selectRT = document.querySelector('select')
    const options = document.querySelectorAll('option')
    const table = document.querySelector('#squad-table')
    
    const items = document.querySelectorAll('.squad-item')
    selectRT.addEventListener('change', setSquad)
    
    const row = table.rows
    for(let i = 1; i < row.length; i++)
        row[i].cells[0].textContent = i
        
    
    

    function setSquad(e){
        const src = selectRT.value
        console.log(src);
        
        items.forEach(item => {
            if(src == "all"){
                item.style.display = 'table-row'
            }
            else{
                if(item.classList[0] === src)
                    item.style.display = 'table-row'
                else
                    item.style.display = 'none'
            }
            
        })
    }
})