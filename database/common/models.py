from peewee import SqliteDatabase, Model, IntegerField, TextField

db = SqliteDatabase('people.db')
db_quiz = SqliteDatabase('Quiz.db')


class ModelBase(Model):
    class Meta:
        database = db


class History(ModelBase):
    class Meta:
        db_table = 'History'

    telegram_id = IntegerField()
    region = TextField()
    name = TextField()
    address = TextField()
    destination = TextField()
    star = TextField()
    rating = TextField()
    info = TextField()
    photo = TextField()
    datatime = TextField()


class ModelQuiz(Model):
    class Meta:
        database = db_quiz


class Quiz(ModelQuiz):
    class Meta:
        db_table = 'Quiz'

    question = TextField()
    answer = TextField()


def create_db():
    db.create_tables([History])
    db_quiz.create_tables([Quiz])


if __name__ == '__main__':
    create_db()
