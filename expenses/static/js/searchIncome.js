const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector('.tableOutput')
tableOutput.style.display = 'none'

const mainTable = document.querySelector('.mainTable')
const paginationBlock = document.querySelector('.paginationBlock')

const noResults = document.querySelector('.no-results')
const tabBody = document.querySelector('.tabBody')

searchField.addEventListener('keyup', (e) => {
    const searchVal = e.target.value
    tabBody.innerHTML = ""
    if (searchVal.trim().length > 0) {
        paginationBlock.style.display = 'none'
        fetch("/income/search-param", {
            body: JSON.stringify({ searchText: searchVal }),
            method: 'POST',
        }).then(res => res.json()).then((data) => {
            console.log("data", data);
            mainTable.style.display = 'none'
            tableOutput.style.display = 'block'
            if (data.length === 0) {
                noResults.style.display = 'block'
                tableOutput.style.display = "none"
            } else {
                noResults.style.display = 'none'
                data.forEach(element => {
                    tabBody.innerHTML += `
                    <tr>
                    <th scope="row">${element.amount}</td>
                    <td>${element.source}</td>
                    <td>${element.description}</td>
                    <td>${element.date}</td>
                    <td>                   
                     <a href="./edit-income/${element.id}" class="btn btn-info" > <i class="fa-solid fa-pen-to-square"></i></a>
                     <a href="./delete-income/${element.id}" class="btn btn-danger" > <i class="fa-solid fa-trash"></i></a>
                    </td>
                    
                    </tr>`
                });

            }
        })

    } else {
        tableOutput.style.display = 'none'
        mainTable.style.display = 'block'
        paginationBlock.style.display = 'block'
    }
})