document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector('#search-input')
    const itemsList = document.querySelector('#items-list')
    const items = []
    const selectedTeamForm = document.querySelector('#team-id')


    searchInput.addEventListener('keyup',real_time_search_show_items)

    function real_time_search(e){
        item = e.target
        searchInput.value = item.textContent
        selectedTeamForm.value = item.id
        giveAllItemsHiddenClass()
    }

    function real_time_search_show_items(e){
        if(searchInput.value.trim()=== ""){
            giveAllItemsHiddenClass()
        }else{
            items.forEach(item => {
                if(item.textContent.toLowerCase().trim().includes(searchInput.value))
                    item.classList.remove('hidden')
                else
                    item.classList.add('hidden')
            })
        }
    }


    function giveAllItemsHiddenClass(){
        items.forEach(item => {
            item.classList.add('hidden')
        })
    }


    fetch('/teamsapi/')
        .then(response => response.json())
        .then(data => {
            Teams = Array.from(new Set(data.map(item => JSON.stringify(item))))
                .map(item => JSON.parse(item));
            Teams.forEach(item => {
               let i = document.createElement('li') 
               i.classList.add('items')
               i.classList.add('hidden')
               i.id = item['id']
               i.textContent = item['shortname']
               itemsList.appendChild(i)
               items.push(i)
               i.addEventListener('click',real_time_search)
            });    
            // document.querySelectorAll('.inner-div')[4].classList.add('mask-id')
            
        });

        
});
