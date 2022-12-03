/*This script controls the interactivity of the viewer application.*/
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array
}

const QUEUE = shuffle(Object.keys(TIKTOKS));
//Shuffle the list of TikToks' IDs to determine the order in which to show them.
var queue_pointer = 0;
load_tiktok(TIKTOKS[QUEUE[queue_pointer]]);



function initialize_history(){window.localStorage["jimtok-history"] = "[]";}
function clear_history(){
    window.localStorage.clear("jimtok-history");
    document.querySelector("#history-list").innerHTML = "";
    initialize_history();
}
function read_history(){
    try{
        return JSON.parse(window.localStorage["jimtok-history"]);
    } catch(e){
        initialize_history();
        return JSON.parse(window.localStorage["jimtok-history"]);
    }
}
function write_history(history){window.localStorage["jimtok-history"] = JSON.stringify(history);}
function create_history_listing(video_id){
    return `<li><a onclick="load_tiktok(TIKTOKS['${video_id}'])">${video_id}</a></li>`;
}
function push_history(video_id){
    h = read_history();
    h.push(video_id);
    write_history(h);
    document.querySelector("#history-list").innerHTML += create_history_listing(video_id);
}
/*Crete functions to track viewing history.*/



function switch_tabs(tab){
    for(element of document.querySelectorAll(".sidebar-content")){
        element.style.setProperty("display","none");
    }
    //Hide all other content.
    document.getElementById(tab).style.setProperty("display","flex");
    //Display the content corresponding to the selected tab.
}

document.querySelector("#info-tab").addEventListener("click",function(){switch_tabs("info");});
document.querySelector("#history-tab").addEventListener("click",function(){switch_tabs("history");});
document.querySelector("#search-tab").addEventListener("click",function(){switch_tabs("search");});


function generate_comment_html(comment){
    return `<div class="comment">
        <b>${comment["commenter-username"]} · ${comment["time-posted"]}</b><br />
        ${comment["comment-text"]}
        <br /><hr />
    </div>`;
}


function load_tiktok(info){
    document.querySelector("video").src = `${DATA_PATH}videos/${info["id"]}.mp4`;
    document.querySelector("#username").innerText = `${info["creator-nickname"]} (${info["creator-username"]}) · ${info["time-posted"]}`;

    document.querySelector("#music-title").innerText = info["music-title"];

    document.querySelector("#video-id").innerText = `ID: ${info["id"]}`;

    document.querySelector("#n-likes").innerText = info["like-count"];
    document.querySelector("#n-comments").innerText = info["comment-count"];

    comment_string = "";
    for(comment of info["comments"]){
        comment_string += generate_comment_html(comment);
    }
    document.querySelector("#comments").innerHTML = comment_string;

    push_history(info["id"]);
    //Add video to viewing history.

}


function next_tiktok(){
    queue_pointer = Math.min(queue_pointer+1, QUEUE.length-1);
    load_tiktok(TIKTOKS[QUEUE[queue_pointer]]);
    //Move the queue pointer 1 forward and load the video.
}

function prev_tiktok(){
    queue_pointer = Math.max(queue_pointer-1, 0);
    load_tiktok(TIKTOKS[QUEUE[queue_pointer]]);
    //Move the queue pointer 1 backward and load the video.
}


document.addEventListener("keyup",function(e){
    if(e.key=="ArrowDown"||e.key=="ArrowRight"){
        next_tiktok();
    } else if (e.key=="ArrowUp"||e.key=="ArrowLeft"){
        prev_tiktok();
    } else if (e.key==" "){
        if (document.querySelector("video").paused){
            document.querySelector("video").play();
        } else {
            document.querySelector("video").pause();
        }

    }
})
