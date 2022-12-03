/*This script implements the ranked retrieval used in the search feature of the
viewer application.*/

function normalize(text, ngram_size=5){
    text = text.toLowerCase();
    text = text.replaceAll(/[\s/—]+|-{2,}/g, " ");
    text = text.replaceAll(/[^\w@# ]/g, "");

    let tokens = [];
    for(i=0;i<=(text.length-ngram_size);i++){
        let ngram = text.substring(i,i+ngram_size);
        tokens.push(ngram);
    }
    return tokens
}

function vectorize_query(query,method="binary"){
    let query_tokens = normalize(query);

    let query_vector = {};

    switch(method){
        case "count":
            break;
        default:
            for(term of query_tokens){
                query_vector[term] = 1;
            }
    }
    return query_vector;

}

function similarity_rank(query,query_method="binary",document_method="tf-idf"){

    let query_vector = vectorize_query(query);

    let similarity_scores = {};

    for([q_term, q_component] of Object.entries(query_vector)){
        if (!INDEX.hasOwnProperty(q_term)){
            continue;
            //Skip query terms that are not in the vocabulary of the corpus.
        }

        for(posting of INDEX[q_term]){
            let docid = posting[0];
            let tf = posting[1];
            let idf = Math.log2(Object.keys(TIKTOKS).length/INDEX[q_term].length);//log2(N/df)
            similarity_scores[docid] = tf*idf * q_component;
        }

    }

    ranked_list = [];
    for(docid in similarity_scores){
        ranked_list.push([docid, similarity_scores[docid]]);
    }

    ranked_list.sort(function(a, b) {
        return -(a[1] - b[1]);
    });

    return ranked_list

}

function create_ranked_list_html(ranked_list){
    let output = "";
    for(listing of ranked_list){
        let id = listing[0];
        let score = listing[1];
        output += `<li><a onclick="load_tiktok(TIKTOKS['${id}'])">${id}</a> (score: ${score})</li>`;
    }
    document.querySelector("#search-results").innerHTML = output;

}

document.querySelector("#search-bar").addEventListener("keyup",function(e){
    if(e.key=="Enter"){
        create_ranked_list_html(similarity_rank(
            document.querySelector("#search-bar").value
        ));
    }
});
