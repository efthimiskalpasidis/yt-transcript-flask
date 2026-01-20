CREATE TABLE transcripts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    youtube_url TEXT NOT NULL,
    content MEDIUMTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_youtube_url (youtube_url(255))
);