
async function loadComments(pr_number, comments_url)
{
    // If colapse is open, button was clicked to close it. No need to load comments.
    var colapse = document.getElementById("collapse-comments-" + pr_number)
    if(colapse.classList.contains("show"))
        return;
    
    var commentsPreloader = document.getElementById("comments-preloader-" + pr_number)
    commentsPreloader.innerHTML = "Loading..."

    var result = []
    var page = []
    var pageIndex = 1
    
    do
    {
        var response = await fetch(comments_url + "?page=" + pageIndex)
        var page = await response.json()
        result = result.concat(page)
        pageIndex++
    } while(page.length != 0)

    var commentsCount = result.length

    // Take only last 10 comments
    result = result.slice(Math.max(result.length - 10, 0))

    // Reverse because we want to see newest comments at the top
    result = result.reverse()

    var hiddenCommentsCount = commentsCount - result.length
    
    var commentsContainer = document.getElementById("comments-container-" + pr_number)
    commentsContainer.innerHTML = createCommentsList(result)

    if(hiddenCommentsCount != 0)
        commentsPreloader.innerHTML = hiddenCommentsCount + " hidden comments (newest at the top)"
    else
        commentsPreloader.innerHTML = "No hidden comments (newest at the top)"
        // commentsPreloader.style.display = "none"

    localStorage.setItem('viewd_at_' + pr_number, new Date().toISOString())
    setBlueBarIfVisited()
}

function createCommentsList(comments)
{
    var result = []

    comments.forEach(comment => {
        var date = new Date(comment.created_at)
        date = formatDate(date)

        var body = comment.body
        
        // Replace possibly PR references (#number) with url
        var regex = /( )(#)([0-9]+)/ig
        body = body.replace(regex, "$1<a href='" + getRepoUrl() + "$3" + "' target='_blank'>$2$3</a>")

        // Make urls clickable
        var regex = /([^"']|^)(https?:\/\/[-\w.%&?/:_@#=+;]+[^."')\s ])/ig
        body = body.replace(regex, "$1<a href='$2' target='_blank'>$2</a>")
        
        // Replace line breaks
        body = body.replace(/\n/ig, "<br>")

        // Replace code tags
        var regex = /`(.*?)`/ig
        body = body.replace(regex, "<code>$1</code>")

        // Bold usernames
        var regex = /(@[a-z\d]+-*[a-z\d]+)/ig
        body = body.replace(regex, "<strong>$1</strong>")

        result += `
        <div class="pt-3 border-top">
            <img class="rounded pull-left" style="width: 32px; height: 32px;" src="` + comment.user.avatar_url + `">
            <div class="media-body small text-muted pl-5">
                <div class="row">
                    <div class="col-auto"><strong class="text-gray-dark">` + comment.user.login + `</strong></div>
                    <div class="col-auto">` + date + `</div>
                    <div class="col text-right2"><a href="` + comment.html_url + `" target="_blank" class="no-color-link">View on Github</a></div>
                </div>
                <div class="row word-break mr-2">
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

function showError(message)
{
    document.querySelector('#error-modal-body').innerText = message
    $('#error-modal').modal()
}

// Action handlers
async function actionRunTests(url, access_token, author, pr_number)
{
    url = url + "?access_token=" + access_token
    await postComment(url, "please test", pr_number)
}

async function actionAskForIntroduction(url, access_token, author, pr_number)
{
    url = url + "?access_token=" + access_token
    await postComment(url, "Hi @" + author + ", I can't seem to find you in [DQM contacts list](https://twiki.cern.ch/twiki/bin/viewauth/CMS/DQMContacts). Could you please briefly introduce yourself?", pr_number)
}

async function actionAskForSubsystemName(url, access_token, author, pr_number)
{
    url = url + "?access_token=" + access_token
    await postComment(url, "Hi @" + author + ", could you please make sure that subsystem name appears in the title of the PR?", pr_number)
}

async function actionReject(url, access_token, author, pr_number)
{
    url = url + "?access_token=" + access_token
    await postComment(url, "-1", pr_number)
}

async function actionSign(url, access_token, author, pr_number)
{
    url = url + "?access_token=" + access_token
    await postComment(url, "+1", pr_number)
}

async function postComment(url, comment, pr_number)
{
    $("#pr-card-" + pr_number).fadeTo("fast", 0.5)
    
    var response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify({body: comment}),
    })

    if(response.status != 201)
    {
        showError(await response.text())
    }

    $("#pr-card-" + pr_number).fadeTo("slow", 1)

    return response
}

// Set blue bar if visited initially
window.onload = function(e)
{
    setBlueBarIfVisited();
}

function setBlueBarIfVisited()
{
    pr_cards = document.querySelectorAll(".pr-card")
    pr_cards.forEach(function(card) 
    {
        var pr_number = card.dataset.prNumber
        var updated_at = new Date(card.dataset.updatedAt);
        var viewd_at = new Date(localStorage.getItem('viewd_at_' + pr_number));
        
        if(updated_at > viewd_at)
        {
            card.classList.add("vertical-strip")
        }
        else
        {
            card.classList.remove("vertical-strip")
        }
    });
}

$("[data-toggle=tooltip]").tooltip();
