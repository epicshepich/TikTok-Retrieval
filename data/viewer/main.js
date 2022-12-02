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
