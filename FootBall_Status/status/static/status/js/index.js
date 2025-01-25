document.addEventListener('DOMContentLoaded', function () {

const lg_Box = document.querySelectorAll('.League-Box')
console.log(lg_Box.length);

const matchesBtn = document.querySelectorAll('.choose-match-toDisply-btn');
const match_0 = document.querySelector('.matches-1');
const match_1 = document.querySelector('.matches-2');
matchesBtn.forEach(btn => {
    btn.addEventListener('click', (e) => {
        if(e.target == matchesBtn[0]){
            match_0.style.display = 'inline-block';
            match_1.style.display = 'none';
                
        }
        else{
            match_0.style.display = 'none';
            match_1.style.display = 'inline-block';
        }
    })
})


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