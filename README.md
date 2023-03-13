# Простая программа для управления личными финансами
## Описание программы
Представленная в данном репозитории программа запускается из файла main.py для базы данных, задаваемой DB_NAME = "test.db" (10 строчка). 

### Основное окно программы: 

В основном окне программы представлена таблица расходов, таблица бюджета и кнопки для управления базой данных. 

![image](https://user-images.githubusercontent.com/83416875/224791387-fb9c7b44-f7f4-469b-b36a-d861d93d58d7.png)

### Фунции управления базой данных: 
* Добавление расхода
Для добавления расхода необходимо выбрать категорию из выпадающего списка, ввести сумму расхода и комментарий (по желанию). Добавленная сумма отражается в изменении колонки "summ" (потраченная сумма за определенный период) в таблице бюджета

* Удаление расхода

Для удаления расхода необходимо выбрать соответствующие расходы в таблице расходов (можно несколько) и нажать на кнопку "Удалить выбранный расход"

* Изменение бюджета

Изменение бюждета происходит независимо на день/недедю/месяц. Изменения отражается в колонке "budget" в таблице бюждета

* Изменение списка категорий

Изменение списка категорий происходит в отдельном окне, открывающемся при нажатии кнопки "Редактировать категории" основного окна. 

![image](https://user-images.githubusercontent.com/83416875/224794439-c679c107-2340-4505-a8c6-d801c1252f5f.png)

Функции: 
- изменение названия категории происходит при двойном нажатии на соответствующую категорию
- добавление категории: если желаемая категория дочерняя к уже умеющейся, то необходимо выбрать соответствующую имеющуюся категорию и нажать кнопку "Добавить". При этом откроется окно для ввода названия новой категории, необходимо ввести его и нажать "ок". Категория добавится как дочерняя к данной. Если же новая категория не дочерняя, необходимо проделать те же действия без предварительного выбора имеющейся категории

![image](https://user-images.githubusercontent.com/83416875/224795428-70328a06-78fb-4c1e-8e44-e86b914b9d04.png)


- удаление категории: происходит при выборе желаемой категории для удаления и нажатии на кнопку "удалить". (!) если у категории имелись дочерние, то они также удалятся

После внесения всех желаемых изменений необходимо нажать кнопку "ок" для закрытия окна редактирования категорий и перехода к основному окну. 

Желаю Вам приятного использования программы!


____________________________________________________________________________________________________________________
#### (учебный проект для курса по практике программирования на Python)

[Техническое задание](specification.md)

Архитектура проекта строится на принципе инверсии зависимостей. Упрощенная схема
классов выглядит так:
![](structure.png)

Для хранения данных используется паттерн Репозиторий. Структура файлов
и каталогов (модулей и пакетов) отражает архитектуру:

📁 bookkeeper - исполняемый код 

- 📁 models - модели данных

    - 📄 budget.py - бюджет
    - 📄 category.py - категория расходов
    - 📄 expense.py - расходная операция
- 📁 repository - репозиторий для хранения данных

    - 📄 abstract_repository.py - описание интерфейса
    - 📄 memory_repository.py - репозиторий для хранения в оперативной памяти
    - 📄 sqlite_repository.py - репозиторий для хранения в sqlite (пока не написан)
- 📁 view - графический интерфейс (пока не написан)
- 📄 simple_client.py - простая консольная утилита, позволяющая посмотреть на работу программы в действии
- 📄 utils.py - вспомогательные функции

📁 tests - тесты (структура каталога дублирует структуру bookkeeper)

Для работы с проектом нужно сделать fork и склонировать его себе на компьютер.

Проект создан с помощью poetry. Убедитесь, что poetry у вас установлена
(инструкцию по установке можно посмотреть [здесь](https://python-poetry.org/docs/)).
Для установки всех зависимостей, запустите (убедитесь, что вы находитесь
в корневой папке проекта - там, где лежит файл pyproject.toml):

```commandline
poetry install
```

Для запуска тестов и статических анализаторов используйте следующие команды (убедитесь, 
что вы находитесь в корневой папке проекта):
```commandline
poetry run pytest --cov
poetry run mypy --strict bookkeeper
poetry run pylint bookkeeper
poetry run flake8 bookkeeper
```

При проверке работы будут использоваться эти же инструменты с теми же настройками.

Задача первого этапа:
1. Сделать fork репозитория и склонировать его себе на компьютер
2. Написать класс SqliteRepository
3. Написать тесты к этому классу
4. Подключить СУБД sqlite к simple_client (пока он работает в оперативной памяти и все забывает при выходе)

Задача второго этапа:
1. Создать виджеты:
   - для отображения списка расходов с возможностью редактирования
   - для отображения бюджета на день/неделю/месяц с возможностью редактирования
   - для добавления нового расхода
   - для просмотра и редактирования списка категорий
2. Собрать виджеты в главное окно

В итоге окно должно выглядеть примерно так:

![](screenshot.png)

Воспроизводить данный дизайн в точности не требуется, вы можете использовать другие
виджеты, другую раскладку. Дизайн, представленный на скриншоте, предполагает, что 
редактирование списка категорий будет выполняться в отдельном окне. Вы можете
сделать так же, а можете все разместить в одном окне, использовать вкладки
или контекстные меню. Важно только реализовать функциональность.

Задачей этого этапа не является подключение реальной логики приложения и базы
данных. Пока нужно только собрать интерфейс. Файлы, описывающие интерфейс,
должны располагаться в папке bookkeeper/view.

Задача 3 этапа:
1. Написать тесты для графического интерфейса
2. Создать реализацию компонента Presenter модели MVP, тем самым соединив все компоненты
в работающее приложение.

Итогом 3 этапа должно быть полностью работающее приложение, реализующее всю требуемую
функциональность.

Задача 4 этапа:
1. Доделать, отдалить и привести в порядок все, что было сделано на предыдущих этапах
2. Добавить стилизацию (не влияет на оценку).
3. Добавить дополнительные функции (не влияет на оценку). Например:
    - возможность задать бюджет на день с переносом остатка на следующий день
    - формирование отчета за произвольный период
    - интерактивная визуализация данных в отчете
    - возможность добавления чека по qr-коду или скану
    - и т.д.

Реализация дополнительных функций и стилизация приложения не влияют на оценку, поэтому
сосредоточиться следует на том, чтобы основная функциональность хорошо работала
и код был хорошо написан.

Для сдачи работы достаточно прислать ссылку на свой форк в форму "Добавить ответ на задание" в ЛМС, 
pull-request создавать не надо.
