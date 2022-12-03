#This script is used to generate a basic index to enable search within the
#viewing application.
using JSON
using Unidecode

function normalize(document::String;
        ngram_size=5,
        replacements=[(r"[\s/—]+|-{2,}"," "), (r"[^\w@# ]",""), (!isascii,"")],
        #Replace all delimiter-ish characters with a single space.
        #Remove all non-alphanumeric characters except @, #, and space.
        case_folding=lowercase
    )
    document = unidecode(document)
    #Decode unicode back into a UTF-8 String.
    document = case_folding(document)
    for (pattern, replacement) in replacements
        document = replace(document, pattern => replacement)
    end

    tokens = String[
        join(document[i:j])
        for (i,j) in
        zip(
            1:(length(document)-ngram_size),
            ngram_size:length(document)
        )
    ]
    #Generate n-grams of the specified size.

    return tokens
end


tiktoks = JSON.parsefile("cleaned_master.json",use_mmap=false)

index = Dict{String,Vector{ Vector{Union{String,Int}} }}()

for (i,(id,tiktok)) in enumerate(tiktoks)
    println("Indexing TikTok $(i) / $(length(tiktoks))")

    document = join([
        string(tiktok["creator-username"]),
        string(tiktok["creator-nickname"]),
        string(tiktok["description"]),
        string(tiktok["coverphoto-ocr"]),
        string(tiktok["speech-to-text"]),
        string(tiktok["id"]),
        string(tiktok["music-title"]),
        [string(comment["commenter-username"])*" "*string(comment["comment-text"]) for comment in tiktok["comments"]]...
    ], " ")


    term_frequencies = Dict{String,Int}()
        #For a given document, we construct a dict of the term frequencies.
        for term in normalize(document)
            #Normalize the raw document into a sequence of terms.
            if haskey(term_frequencies,term)
                term_frequencies[term] += 1
            else
                term_frequencies[term] = 1
            end
            #Tally each term as it appears in the normalized sequence of terms.
        end
        for (term,term_frequency) in term_frequencies
            if haskey(index,term)
                push!(index[term], [id,term_frequency])
            else
                index[term] = [[id,term_frequency]]
            end
            #If the term is already in the index, simply add a posting for this
            #document. Otherwise, initialize the postings list with this posting.
        end

end


open("basic_index.json","w") do f
    JSON.print(f,index)
end
