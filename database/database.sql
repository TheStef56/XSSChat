DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `id` varchar(36) PRIMARY KEY DEFAULT (UUID()),
    `username` varchar(50) NOT NULL,
    `email` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `token` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` varchar(36) NOT NULL,
    `username` varchar(50) NOT NULL,
    `message` varchar(4096) NOT NULL,
    `date` DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
