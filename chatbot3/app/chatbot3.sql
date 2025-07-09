CREATE TABLE chat_history ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    user_message TEXT NOT NULL, 
    bot_response TEXT NOT NULL, 
    temperature FLOAT DEFAULT 1.0, 
    top_p FLOAT DEFAULT 1.0, 
    presence_penalty FLOAT DEFAULT 0.0, 
    frequency_penalty FLOAT DEFAULT 0.0, 
    max_tokens INT DEFAULT 500, 
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP 
);