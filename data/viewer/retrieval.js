/*This script implements the ranked retrieval used in the search feature of the
viewer application.*/

function normalize(text){

}

function vectorize_query(q,method="binary"){
    query_tokens = normalize(query);

    query_vector = {};

    switch(method){
        case "count":
            break;
        default:
            for(term of query_tokens){
                query_vector[term] = 1;
            }
    }

}

function similarity_rank(query,corpus,query_method="binary",document_method="tf-idf"){

    query_vector = vectorize_query(query);

    similarity_scores = {};

    for([q_term, q_component] of Object.entries(query_vector)){
        if (!corpus.hasOwnProperty(q_term)){
            continue;
            //Skip query terms that are not in the vocabulary of the corpus.
        }

        for(posting of corpus[q_term]){
            docid = posting[0];
            tf = posting[1];
            similarity_scores[docid] = tf * q_component;
        }

    }

}
