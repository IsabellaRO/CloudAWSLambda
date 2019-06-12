DROP TABLE IF EXISTS Jobs;

CREATE TABLE Jobs (
    jobId INT AUTO_INCREMENT NOT NULL,
    uid INT NOT NULL,
    status VARCHAR(255) NOT NULL,
    result VARCHAR(255),
    PRIMARY KEY(jobId)
);

INSERT INTO Jobs (uid, status, result) VALUES (0, "DONE", "5");

SELECT * FROM Jobs;