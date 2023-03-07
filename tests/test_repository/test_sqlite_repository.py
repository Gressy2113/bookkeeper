from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository

cat_repo = SQLiteRepository[Category]("test.db", Category)
# all_ = cat_repo.get_all({'parent' : '1', 'name' : 'мясо', 'pk': 2})
# for i in all_:
#     print(i)
# cat_repo.delete(7)
print(cat_repo.get_all())
