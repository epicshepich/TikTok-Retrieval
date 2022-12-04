<!DOCTYPE html>
<html>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<head>
    <link rel="stylesheet" type="text/css" href="./style.css">
    <link id="favicon" rel="shortcut icon" type="image/x-icon" href="./favicon.ico">
    <script src="./svg_icons.js"></script>
    <script>
        document.querySelector("#favicon").href = favicon;
    </script>
    <title>JimTok</title>
</head>

<body>

<?php
ini_set('memory_limit', '1024M');
//Increase memory size limit for index.
$DATA_PATH = "./";
if (!file_exists($DATA_PATH."/cleaned_master.json")) {
    $DATA_PATH = "../";
}
//If the data aren't in the same directory as the viewer, then the viewer is
//nested in a separate folder.);
//Use all forward slashes.
echo "<script>const DATA_PATH = '".$DATA_PATH."';const TIKTOKS = ".file_get_contents(__DIR__."/".$DATA_PATH."cleaned_master.json").";</script>";
?>

<div id="main-container">
    <div id="video-container">
        <video id="video" src="../videos/6849128516101917957.mp4" controls autoplay loop></video>
    </div>

    <div id="sidebar">
        <div id="tab-selector">
            <div id="info-tab" class="tab">Info</div>
            <div id="history-tab" class="tab">View History</div>
            <div id="search-tab" class="tab">Search</div>
        </div>

        <div id="info" class="sidebar-content">
            <div id="summary-info" class="info-field">
                <span id="username"></span>
                <br />
                <span id="video-id"></span>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <span id="svg-heart"></span>
                <span id="n-likes"></span>
                &nbsp;
                <span id="svg-comments"></span>
                <span id="n-comments"></span>
                <br /><hr / />
                <span id="description"></span>

            </div>
            <script>
                document.querySelector("#svg-heart").innerHTML = svg_heart;
                document.querySelector("#svg-comments").innerHTML = svg_comments;
            </script>

            <div id="music" class="info-field">
                <span id="svg-music-notes"></span>
                <span id="music-title"></span>
            </div>
            <script>
                document.querySelector("#svg-music-notes").innerHTML = svg_music_notes;
            </script>



            <div id="comments" class="info-field">
            </div>


        </div>

        <div id="history" class="sidebar-content">
            <button id="clear-history" onclick="clear_history()">Clear History</button>
            <ol id="history-list">
            </ol>
        </div>

        <div id="search" class="sidebar-content">
            <div id="search-bar-container"><input type="text" id="search-bar"/></div>
            <div id="search-results-container">
                <ol id="search-results">
                </ol>
            </div>
        </div>
    </div>



</div>



</body>

<script src="./main.js"></script>
<?php echo "<script>const INDEX = ".file_get_contents(__DIR__."/".$DATA_PATH."basic_index.json").";</script>";?>
<!--Load the index and retrieval code after the rest of the page has loaded.-->
<script src="./retrieval.js"></script>

</html>
