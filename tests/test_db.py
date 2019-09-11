import datetime

from corelib.db import PropsItem, PropsMixin, DatePropsItem


class TestPropsMixin:

    def test_insert(self):
        class Book(PropsMixin):
            def __init__(self):
                self.id = id(self)

            title = PropsItem(name='title')
            date = DatePropsItem(name='date')

            def get_uuid(self):
                return '/bran/{0.__class__.__name__}/{0.id}'.format(self)

        book1 = Book()
        book1.title = '牛逼哄哄'
        book1.date = '2019-09-11'
        assert book1.title == '牛逼哄哄'
        assert book1.date == datetime.datetime.strptime('2019-09-11', '%Y-%m-%d').date()
        assert book1.id == id(book1)

        book2 = Book()
        book2.title = '天池'
        book2.date = '2019-09-10'
        assert book2.title == '天池'
        assert book2.date == datetime.datetime.strptime('2019-09-10', '%Y-%m-%d').date()
        assert book2.id == id(book2)

        assert book1.title == '牛逼哄哄'
        assert book1.date == datetime.datetime.strptime('2019-09-11', '%Y-%m-%d').date()
        assert book1.id == id(book1)
