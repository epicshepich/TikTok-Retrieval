function sleep(ms) {
    /*Call `await sleep()` to synchronously block the execution of the
    next line for an input duration, in milliseconds. Copied from:
        https://www.tutorialspoint.com/javascript-sleep-function.
    */
    return new Promise(resolve => setTimeout(resolve, ms));
}

function next_tiktok(){
    $("button[data-e2e='arrow-right']").click();
    //Simulate a click on the button that skips to the next video.
}

function prev_tiktok(){
    $("button[data-e2e='arrow-left']").click();
    //Simulate a click on the button that skips to the previous video.
}

function extract_tiktok_info(){
    let info = {};
    info["video-src"] = $("video").src;
    info["coverphoto-src"] = $("img[mode='2']").src;

    info["permalink"] = $("[data-e2e='browse-video-link']").innerText;
    info["web-id"] = info["permalink"].match(/web_id=(?<web_id>\d+)/).groups.web_id;
    info["id"] = info["permalink"].match(/video\/(?<id>\d+)/).groups.id;
    //Extract the ID from the link.

    info["like-count"] = $("[data-e2e='browse-like-count']").innerText;
    info["comment-count"] = $("[data-e2e='browse-comment-count']").innerText;

    info["username"] = "@" + $("[data-e2e='browse-username']").innerText;
    nickname_field = $("[data-e2e='browser-nickname']").innerText;
    info["nickname"] = nickname_field.split("\n·\n")[0];
    info["posted"] = nickname_field.split("\n·\n")[1];

    music_field = $("[data-e2e='browse-music']").children[0];
    info["music-title"] = music_field.innerText;
    info["music-src"] = music_field.href;

    info["description"] = $("[data-e2e='browse-video-desc']").innerText;

    info["scrape-timestamp"] = Date.now();

    return info;
}


async function scrape_tiktoks(n_to_scrape, delay=1000){
    let tiktoks = [];
    for(i=0;i<n_to_scrape;i++){
        tiktoks.push(extract_tiktok_info());
        await sleep(delay);
    }
    return tiktoks;
}
