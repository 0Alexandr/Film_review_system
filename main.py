from datetime import date


movie_title = "Интерстеллар"
user_name = "Алексей"

# Списки для хранения оценок и отзывов
ratings_list = [9, 10]
reviews_list = ["Отличный фильм!", "Потрясающий сюжет"]


# ФУНКЦИЯ 1: Расчет рейтинга 
def get_average_rating():
    average = sum(ratings_list) / len(ratings_list)
    return round(average, 1)


# ФУНКЦИЯ 2: Оценка и рецензирование 
def add_new_review(new_rating, new_text):
    # Просто добавляем новую оценку и текст в наши списки
    ratings_list.append(new_rating)
    reviews_list.append(new_text)
    print("Система: Ваш отзыв и оценка успешно добавлены!")


# ФУНКЦИЯ 3: Управление каталогом (Вывод информации)
def print_movie_info():
    print(f"\n Фильм: {movie_title}")
    print(f" Средний рейтинг: {get_average_rating()}/10")
    print(f" Последний отзыв от {user_name}: {reviews_list[-1]}")


# 1. Показываем информацию о фильме вначале
print("--- Информация до изменения ---")
print_movie_info()

# 2. Добавляем новую оценку (например, 8) и новый отзыв
print("\n--- Добавляем новый отзыв ---")
add_new_review(8, "Хорошее кино, но затянуто.")

# 3. Показываем информацию снова (рейтинг сам пересчитался, отзыв обновился)
print("\n--- Информация после изменения ---")
print_movie_info()