let articlesByTime = document.getElementById('articles-by-time')

let articlesByViews = document.getElementById('articles-by-views')

articlesByViews.hidden = true

time.onclick = (e) => {
    articlesByTime.hidden = false
    articlesByViews.hidden = true
    time.classList.add('checked')
    views.classList.remove('checked')
}

views.onclick = (e) => {
    articlesByTime.hidden = true
    articlesByViews.hidden = false
    views.classList.add('checked')
    time.classList.remove('checked')
}