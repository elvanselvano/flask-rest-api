
-- @BLOCK
create table employee (
  id int AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(20) UNIQUE,
  full_name VARCHAR(20),
  gender ENUM('M', 'L'),
  married tinyint
)

-- @BLOCK