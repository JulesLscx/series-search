from api.models import Users, Role, Series, Watched

def test_create_user():
    user = Users('test', 'test', Role.ADMIN)
    assert user.name == 'test'
    #Check that the password is hashed
    assert user.password != 'test'
    assert user.role == Role.ADMIN
    
def test_password_check():
    user = Users('test', 'test', Role.ADMIN)
    assert user.check_password('test')
    assert not user.check_password('wrong_password')

def test_series():
    serie = Series('test')
    assert serie.title == 'test'
    assert serie.idSerie == None
    
def test_watched():
    user = Users('test', 'test', Role.ADMIN)
    serie = Series('test')
    serie.idSerie = 1
    #Can't autoincrement idSerie because not commited to db so idSeries is manually set to 1
    watch = Watched(user,serie)
    assert watch.idUser == 'test'
    assert watch.idSerie == 1
