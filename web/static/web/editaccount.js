document.addEventListener('DOMContentLoaded', () => {
    console.log("hello")
    let account_general = document.getElementById('account-general')
    let change_password = document.getElementById('account-change-password')
    let info = document.getElementById('account-info')
    let notifications = document.getElementById('account-notification')

    links = document.querySelectorAll('a')
    links.forEach(function(link){
        link.addEventListener("click", () => {
            console.log(link.textContent)
        }) 
    });
    

    }
)