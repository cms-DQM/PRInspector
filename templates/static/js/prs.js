
function loadComments(pr_number, comments_url)
{
    // If colapse is open, button was clicked to close it. No need to load comments.
    var colapse = document.getElementById("collapse-comments-" + pr_number)
    if(colapse.classList.contains("show"))
        return;
    
    var commentsPreloader = document.getElementById("comments-preloader-" + pr_number)
    commentsPreloader.innerHTML = "Loading..."
    commentsPreloader.style.display = ""

    var result = []
    var page = []
    var pageIndex = 1
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            page = JSON.parse(xhttp.responseText)
            result = result.concat(page)
            pageIndex++

            if(page.length == 0)
            {
                var commentsCount = result.length

                // Take only last 10 comments
                result = result.slice(Math.max(result.length - 10, 0))

                var hiddenCommentsCount = commentsCount - result.length
                
                var commentsContainer = document.getElementById("comments-container-" + pr_number)
                commentsContainer.innerHTML = createCommentsList(result)

                if(hiddenCommentsCount != 0)
                    commentsPreloader.innerHTML = hiddenCommentsCount+ " hidden comments"
                else
                    commentsPreloader.style.display = "none"
            }
            else
            {
                xhttp.open("GET", comments_url + "?page=" + pageIndex, true);
                xhttp.send();
            }
        }
    };

    xhttp.open("GET", comments_url + "?page=" + pageIndex, true);
    xhttp.send();
}

function createCommentsList(comments)
{
    var result = []

    comments.forEach(comment => {
        var date = new Date(comment.created_at)
        date = formatDate(date)

        var body = comment.body
        body = body.replace(/\n/g, "<br>")

        var regex = /(\b(https?|):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig
        body = body.replace(regex, "<a href='$1' target='_blank'>$1</a>")

        result += `
        <div class="pt-3 border-bottom">
            <img class="rounded pull-left" style="width: 32px; height: 32px;" src="` + comment.user.avatar_url + `">
            <div class="media-body small text-muted">
            <div class="row">
                <div class="col-auto"><strong class="text-gray-dark">` + comment.user.login + `</strong></div>
                <div class="col-auto">` + date + `</div>
                <div class="col text-right2"><a href="` + comment.html_url + `" target="_blank" class="no-color-link">View on Github</a></div>
            </div>
            <div class="row">
                <div class="col"><p>` + body + `</p></div>
            </div>      
            </div>
        </div>`
    });

    return result;
}

function formatDate(date) 
{
    var year = date.getFullYear(),
      month = (date.getMonth() + 1).toString(),
      formatedMonth = (month.length === 1) ? ("0" + month) : month,
      day = date.getDate().toString(),
      formatedDay = (day.length === 1) ? ("0" + day) : day,
      hour = date.getHours().toString(),
      formatedHour = (hour.length === 1) ? ("0" + hour) : hour,
      minute = date.getMinutes().toString(),
      formatedMinute = (minute.length === 1) ? ("0" + minute) : minute,
      second = date.getSeconds().toString(),
      formatedSecond = (second.length === 1) ? ("0" + second) : second;
    return year + "-" + formatedMonth + "-" + formatedDay + " " + formatedHour + ':' + formatedMinute + ':' + formatedSecond;
}