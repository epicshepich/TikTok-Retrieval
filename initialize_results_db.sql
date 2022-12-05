CREATE TABLE indexes(
    index_id INT NOT NULL,
    ngram_size INT,
    sr INT NOT NULL,
    ocr INT NOT NULL,
    comments INT NOT NULL,
    field_attributions INT NOT NULL,
    indexing_time FLOAT NOT NULL,
    storage INT NOT NULL,
    vocab_size INT NOT NULL,
    PRIMARY KEY (index_id)
);

CREATE TABLE experiments(
    experiment_id INT NOT NULL,
    index_id INT NOT NULL,
    term_weight TEXT NOT NULL,
    collection_weight TEXT NOT NULL,
    normalizer TEXT NOT NULL,
    PRIMARY KEY (experiment_id),
    FOREIGN KEY (index_id) REFERENCES indexes(index_id)
);

CREATE TABLE queries(
    query_id INT NOT NULL,
    query_text TEXT NOT NULL,
    target_id TEXT NOT NULL,
    author TEXT NOT NULL,
    useful_description INT NOT NULL,
    comments_on_topic INT NOT NULL,
    purely_visual INT NOT NULL,
    important_lyrics INT NOT NULL,
    subtextual INT NOT NULL,
    PRIMARY KEY (query_id)
);

CREATE TABLE ranking_results(
    experiment_id INT NOT NULL,
    query_id INT NOT NULL,
    retrieval_time FLOAT NOT NULL,
    target_rank INT,
    FOREIGN KEY (query_id) REFERENCES queries(query_id),
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);
