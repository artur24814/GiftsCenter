INSERT INTO users (username, hashed_password, email)
VALUES
  ('test', 'test@mail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'other@mail.com', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO actions (id_user, title, descriptions, date, img)
VALUES
  (1, 'title', 'test title' || x'0a' || 'body', '2018-01-01 00:00:00', 'new_image.png');