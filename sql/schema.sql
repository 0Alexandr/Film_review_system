-- ==========================================
-- КиноОтзыв: структура базы данных SQLite
-- ==========================================

-- Фильмы каталога.
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    genre TEXT NOT NULL,
    director TEXT              -- NULL: режиссёр может быть неизвестен
);

-- Пользователи, оставляющие отзывы.
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    registration_date TEXT NOT NULL    -- дата в формате YYYY-MM-DD
);

-- Отзывы: связывают фильм и пользователя.
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 10),
    text TEXT,                         -- NULL: оценка без текста
    publication_date TEXT NOT NULL,    -- дата в формате YYYY-MM-DD
    recommended INTEGER NOT NULL DEFAULT 1 CHECK (recommended IN (0, 1)),
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
