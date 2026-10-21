-- ==========================================
-- КиноОтзыв: SQL-запросы проекта
-- Значения в условиях (жанр, id, пороги) указаны для проверки в SQLite CLI.
-- В Django-представлениях те же значения передаются параметрами ?.
-- ==========================================


-- ---------- Выборка списков ----------

-- 1. Список всех фильмов каталога по алфавиту
SELECT id, title, year, genre, director
FROM movies
ORDER BY title;

-- 2. Список пользователей по дате регистрации
SELECT id, name, registration_date
FROM users
ORDER BY registration_date, name;

-- 3. Список жанров каталога без повторов (страница поиска)
SELECT DISTINCT genre
FROM movies
ORDER BY genre;


-- ---------- Фильтрация WHERE ----------

-- 4. Фильмы выбранного жанра
SELECT id, title, year, director
FROM movies
WHERE genre = 'Фантастика'
ORDER BY year;

-- 5. Фильмы, вышедшие в 2000–2020 годах, в названии которых есть буква «а»
SELECT id, title, year
FROM movies
WHERE year BETWEEN 2000 AND 2020
  AND title LIKE '%а%'
ORDER BY year DESC;

-- 6. Положительные отзывы: автор рекомендует фильм и ставит не ниже 8
SELECT id, movie_id, user_id, rating, publication_date
FROM reviews
WHERE recommended = 1
  AND rating >= 8
ORDER BY rating DESC, publication_date DESC;

-- 7. Отзывы без текста (только оценка) – проверка NULL
SELECT id, movie_id, rating
FROM reviews
WHERE text IS NULL;


-- ---------- Соединение таблиц JOIN ----------

-- 8. Все отзывы с названием фильма и именем автора (страница «Отзывы»)
SELECT
    reviews.id,
    movies.id AS movie_id,
    movies.title AS movie_title,
    users.name AS user_name,
    reviews.rating,
    reviews.text,
    reviews.recommended,
    strftime('%d.%m.%Y', reviews.publication_date) AS publication_date
FROM reviews
JOIN movies ON reviews.movie_id = movies.id
JOIN users ON reviews.user_id = users.id
ORDER BY reviews.publication_date DESC, reviews.id DESC;

-- 9. Отзывы конкретного фильма с именами авторов (страница фильма)
SELECT
    reviews.id,
    users.name AS user_name,
    reviews.rating,
    reviews.recommended
FROM reviews
JOIN users ON reviews.user_id = users.id
WHERE reviews.movie_id = 1
ORDER BY reviews.publication_date DESC;

-- 10. Полная информация об одном отзыве (страница отзыва)
SELECT
    reviews.id,
    movies.id AS movie_id,
    movies.title AS movie_title,
    movies.genre,
    users.name AS user_name,
    reviews.rating,
    reviews.text,
    reviews.recommended,
    strftime('%d.%m.%Y', reviews.publication_date) AS publication_date
FROM reviews
JOIN movies ON reviews.movie_id = movies.id
JOIN users ON reviews.user_id = users.id
WHERE reviews.id = 4;

-- 11. Последние 5 отзывов (главная страница): ORDER BY + LIMIT/OFFSET
SELECT
    reviews.id,
    movies.title AS movie_title,
    users.name AS user_name,
    reviews.rating
FROM reviews
JOIN movies ON reviews.movie_id = movies.id
JOIN users ON reviews.user_id = users.id
ORDER BY reviews.publication_date DESC, reviews.id DESC
LIMIT 5 OFFSET 0;


-- ---------- Агрегатные функции ----------

-- 12. Общая статистика оценок: количество, среднее, минимум, максимум
SELECT
    COUNT(*) AS reviews_count,
    ROUND(AVG(rating), 1) AS average_rating,
    MIN(rating) AS min_rating,
    MAX(rating) AS max_rating
FROM reviews;

-- 13. Количество фильмов, пользователей и рекомендаций
SELECT
    (SELECT COUNT(*) FROM movies) AS movies_count,
    (SELECT COUNT(*) FROM users) AS users_count,
    (SELECT COUNT(DISTINCT movie_id) FROM reviews) AS rated_movies_count,
    (SELECT SUM(recommended) FROM reviews) AS recommended_count;


-- ---------- Группировка GROUP BY ----------

-- 14. Рейтинг фильмов: средняя оценка и число отзывов (страница «Фильмы»).
--     LEFT JOIN сохраняет фильмы без отзывов (число отзывов = 0).
SELECT
    movies.id,
    movies.title,
    movies.year,
    movies.genre,
    movies.director,
    COUNT(reviews.id) AS reviews_count,
    ROUND(AVG(reviews.rating), 1) AS average_rating
FROM movies
LEFT JOIN reviews ON reviews.movie_id = movies.id
GROUP BY movies.id
ORDER BY average_rating IS NULL, average_rating DESC, movies.title;

-- 15. Статистика по жанрам: фильмы, отзывы и средняя оценка
SELECT
    movies.genre,
    COUNT(DISTINCT movies.id) AS movies_count,
    COUNT(reviews.id) AS reviews_count,
    ROUND(AVG(reviews.rating), 1) AS average_rating
FROM movies
LEFT JOIN reviews ON reviews.movie_id = movies.id
GROUP BY movies.genre
ORDER BY movies_count DESC, movies.genre;

-- 16. Активность пользователей: число отзывов и средняя поставленная оценка
SELECT
    users.name AS user_name,
    COUNT(reviews.id) AS reviews_count,
    ROUND(AVG(reviews.rating), 1) AS average_rating,
    SUM(reviews.recommended) AS recommended_count
FROM users
LEFT JOIN reviews ON reviews.user_id = users.id
GROUP BY users.id
ORDER BY reviews_count DESC, users.name;


-- ---------- Фильтрация групп HAVING ----------

-- 17. Фильмы, у которых не меньше 2 отзывов (страница «Статистика»)
SELECT
    movies.title,
    COUNT(reviews.id) AS reviews_count,
    ROUND(AVG(reviews.rating), 1) AS average_rating
FROM movies
JOIN reviews ON reviews.movie_id = movies.id
GROUP BY movies.id
HAVING COUNT(reviews.id) >= 2
ORDER BY average_rating DESC;

-- 18. Поиск фильмов по жанру, части названия и минимальной средней оценке
--     (страница «Поиск фильмов»; пустая строка означает «без условия»)
SELECT
    movies.id,
    movies.title,
    movies.year,
    movies.genre,
    movies.director,
    COUNT(reviews.id) AS reviews_count,
    ROUND(AVG(reviews.rating), 1) AS average_rating
FROM movies
LEFT JOIN reviews ON reviews.movie_id = movies.id
WHERE ('Фантастика' = '' OR movies.genre = 'Фантастика')
  AND ('' = '' OR movies.title LIKE '%' || '' || '%')
GROUP BY movies.id
HAVING COALESCE(AVG(reviews.rating), 0) >= 8
ORDER BY average_rating DESC, movies.title;
