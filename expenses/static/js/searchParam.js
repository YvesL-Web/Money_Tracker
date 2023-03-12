const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector('.tableOutput')
tableOutput.style.display='none'

const mainTable = document.querySelector('.mainTable')
const paginationBlock = document.querySelector('.paginationBlock')

const tabBody = document.querySelector('.tabBody')

searchField.addEventListener('keyup', (e)=>{
    const searchVal = e.target.value
    tabBody.innerHTML=""
    if(searchVal.trim().length > 0){
        paginationBlock.style.display='none'
        fetch("/outlay/search-param", {
            body: JSON.stringify({ searchText: searchVal }),
            method: 'POST',
        }).then(res => res.json()).then((data) => {
            console.log("data",data);
            mainTable.style.display='none'
            tableOutput.style.display = 'block'
            if(data.length === 0){
                tableOutput.innerHTML="No result found"
            }else{
                data.forEach(element => {
                    tabBody.innerHTML +=`
                    <tr>
                    <th scope="row">${element.amount}</td>
                    <td>${element.category}</td>
                    <td>${element.description}</td>
                    <td>${element.date}</td>
                    </tr>`
                });
              
            }
        })

    }else{
        tableOutput.style.display='none'
        mainTable.style.display = 'block'
        paginationBlock.style.display = 'block'
    }
})