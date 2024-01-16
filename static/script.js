const list = document.querySelectorAll('.item-menu')

function activeLink () {
    list.forEach((item) =>
    item.classList.remove('active'));
    this.classList.add('active');
}
list.forEach((item) =>
item.addEventListener('click', activeLink));





// Remover as divs antigas ao carregar a página
//document.addEventListener('DOMContentLoaded', function () {
//    const container = document.getElementsByClassName('container-interno-sistema-avaliacao');
//    container.innerHTML = ''; // Remove todas as divs antigas
//    container.textContent = '';
//    container.innerText = '';
//});