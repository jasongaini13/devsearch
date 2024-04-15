
    let searchForm = document.getElementById('searchForm');
let pageLinks = document.getElementsByClassName('page-link');

if (searchForm) {
    for (let i = 0; i < pageLinks.length; i++) {
        pageLinks[i].addEventListener('click', function(e) {
            e.preventDefault();
            let page = this.dataset.page;
            let input = document.createElement('input');
            input.setAttribute('type', 'hidden');
            input.setAttribute('name', 'page');
            input.setAttribute('value', page);
            searchForm.appendChild(input);
            searchForm.submit();
        });
    }
}

