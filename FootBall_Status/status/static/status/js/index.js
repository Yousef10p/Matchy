document.addEventListener('DOMContentLoaded', function () {

const lg_Box = document.querySelectorAll('.League-Box')
console.log(lg_Box.length);



lg_Box.forEach((x)=>{

    x.addEventListener('mouseover',()=>{
        x.classList.remove('bg-warning')
        x.classList.add('bg-info')
    })
    
    x.addEventListener('mouseout',()=>{
        x.classList.remove('bg-info')
        x.classList.add('bg-warning')
    })

})



});