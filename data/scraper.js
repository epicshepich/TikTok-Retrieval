function timer(ms) {
    /*Call `await timer()` to synchronously block the execution of the
    next line for an input duration, in milliseconds. Copied from:
        https://www.tutorialspoint.com/javascript-sleep-function.
    */
    return new Promise(resolve => setTimeout(resolve, ms));
}

function next_tiktok(){
    //Simulate a click on the button that skips to the next video.
    document.querySelector("button[data-e2e='arrow-right']").click();
}

function prev_tiktok(){
    //Simulate a click on the button that skips to the previous video.
    document.querySelector("button[data-e2e='arrow-left']").click();
}

function extract_tiktok_info(){
    /*This function extracts information corresponding to the currently
    displayed TikTok including the following:

    - SRC of video tag (for downloading)
    - SRC of cover photo img tag (for downloading)
    - Permalink (for re-accessing)
    - Web ID (I don't really know what this is; but I don't want to skip it
        in case it's important)
    - ID
    - Video like count
    - Video comment count
    - Uploader's username
    - Uploader's nickname
    - Title of music
    - HREF of music a tag
    - Video description text
    - First ~20 top-level comments (including commenter name, comment text, like count, and time posted)
    - Timestamp of info extraction
    */
    let info = {};
    info["video-src"] = document.querySelector("video").src;
    info["coverphoto-src"] = document.querySelector("img[mode='2']").src;

    info["permalink"] = document.querySelector("[data-e2e='browse-video-link']").innerText;
    info["web-id"] = info["permalink"].match(/web_id=(?<web_id>\d+)/).groups.web_id;
    info["id"] = info["permalink"].match(/video\/(?<id>\d+)/).groups.id;
    //Extract the ID from the link.

    info["like-count"] = document.querySelector("[data-e2e='browse-like-count']").innerText;
    info["comment-count"] = document.querySelector("[data-e2e='browse-comment-count']").innerText;

    info["creator-username"] = "@" + document.querySelector("[data-e2e='browse-username']").innerText;
    nickname_field = document.querySelector("[data-e2e='browser-nickname']").innerText;
    info["creator-nickname"] = nickname_field.split("\n·\n")[0];
    info["timeposted"] = nickname_field.split("\n·\n")[1];

    music_field = document.querySelector("[data-e2e='browse-music']").children[0];
    info["music-title"] = music_field.innerText;
    info["music-src"] = music_field.href;

    info["description"] = document.querySelector("[data-e2e='browse-video-desc']").innerText;

    info["comments"] = [];

    top_level_comments = document.querySelectorAll("[data-e2e='comment-level-1']");
    /*This will only grab the first ~20 top-level comments. Have to scroll down
    to get more.*/

    for(comment of top_level_comments){
        replies_field = comment.parentNode.parentNode.parentNode.querySelector("[data-e2e='view-more-1']");

        info["comments"].push({
            "commenter-username":"@"+comment.parentNode.children[0].innerText,
            "comment-text":comment.innerText,
            "time-posted":comment.parentNode.querySelector("[data-e2e='comment-time-1']").innerText,
            "like-count": comment.parentNode.parentNode.querySelector("[data-e2e='comment-like-count']").innerText,
            "replies-count": (replies_field===null) ? "" : replies_field.innerText.match(/\((?<count>\w+)\)/).groups.count
        });
        /*We have to traverse the tree a bit because overall comment containers
        don't have any distinguishing attributes; also, we want the data to be
        linked correctly.*/
    }

    info["scrape-timestamp"] = Date.now() / 1000;
    //Track the time of scraping for data provenance (seconds since epoch).

    return info;
}


async function scrape_tiktoks(n_to_scrape, delay=300){
    /*This function will scrape info for a specified number of TikToks
    and return the results.*/
    let tiktoks = [];
    for(i=0;i<n_to_scrape;i++){
        console.log(i)
        await timer(delay);
        tiktoks.push(extract_tiktok_info());
        await timer(delay);
        next_tiktok();
    }
    return tiktoks;
}

/*
results = await scrape_tiktoks(100, delay=300);
JSON.stringify(results);
*/
