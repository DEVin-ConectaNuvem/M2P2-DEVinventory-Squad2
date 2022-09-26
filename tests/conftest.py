import pytest
from src.app import create_app, db as _db
from src.app.routes import routes
from flask import json
from sqlalchemy import event
from src.app.models.user import User

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

@pytest.fixture(scope="session")
def app():
  app_on = create_app('testing')
  routes(app_on)
  return app_on

@pytest.fixture
def logged_in_client(client):
  data = {
      "email": "luislopes@gmail.com",
      "password": "123Mudar!"
  }

  response = client.post("user/login", data=json.dumps(data), headers=headers)
  return response.json["token"]

@pytest.fixture
def logged_in_client_with_user_deleted(client):
  data = {
      "email": "loivaci.lopes1@example.com",
      "password": "123Mudar!"
  }

  response = client.post("user/login", data=json.dumps(data), headers=headers)
  user = User.query.filter(User.id == 33).first()
  user.roles = []
  _db.session.commit()
  User.query.filter(User.id == 33).delete()
  
  return response.json["token"]

@pytest.fixture(scope="function", autouse=True)
def session(app):
  with app.app_context():
    connection = _db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    sess = _db.create_scoped_session(options=options)
    sess.begin_nested()

    @event.listens_for(sess(), 'after_transaction_end')
    def restart_savepoint(sess2, trans):
      if trans.nested and not trans._parent.nested:
          sess2.expire_all()
          sess2.begin_nested()

    _db.session = sess
    yield sess 
    sess.remove()
    transaction.rollback()
    connection.close()
