CREATE DATABASE IF NOT EXISTS phishing_simulation;

USE phishing_simulation;

CREATE TABLE IF NOT EXISTS interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(50),
    user_agent VARCHAR(255),
    timestamp DATETIME
);
