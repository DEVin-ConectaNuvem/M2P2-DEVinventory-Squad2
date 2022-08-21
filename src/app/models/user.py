import bcrypt 
from src.app import db, ma
from src.app.models.city import City, city_share_schema
from src.app.models.gender import Gender, gender_share_schema
from src.app.models.role import Role, roles_share_schema


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    gender_id = db.Column(db.Integer, db.ForeignKey(Gender.id), nullable = True)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id), nullable = True)
    city_id = db.Column(db.Integer, db.ForeignKey(City.id), nullable = True)
    name = db.Column(db.String(84), nullable = False)
    age = db.Column(db.DateTime, nullable = True)
    email = db.Column(db.String(84), nullable = False, unique=True)
    phone = db.Column(db.String(84), nullable = True)
    password = db.Column(db.String(84), nullable = False)
    cep = db.Column(db.String(84), nullable = True)
    street = db.Column(db.String(84), nullable = True)
    number_street = db.Column(db.String(84), nullable = True)
    complement = db.Column(db.String(84), nullable = True)
    landmark = db.Column(db.String(84), nullable = True)
    district = db.Column(db.String(84), nullable = True)
    gender = db.relationship("Gender", foreign_keys=[gender_id])
    role = db.relationship("Role", foreign_keys=[role_id])
    city = db.relationship("City", foreign_keys=[city_id])

    def __init__(self, gender_id, role_id, city_id, name, age, email, password, phone, cep, street, number_street, complement, landmark, district):
        self.gender_id = gender_id
        self.role_id = role_id
        self.city_id = city_id
        self.name = name
        self.age = age
        self.email = email
        self.password = password
        self.phone = phone
        self.cep = cep
        self.street = street
        self.number_street = number_street
        self.complement = complement
        self.landmark = landmark
        self.district = district

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    @classmethod
    def seed(cls, gender_id, role_id, city_id, name, age, email, password, phone, cep, street, number_street, complement, landmark, district):
        user = User(
        gender_id = gender_id,
        role_id = role_id,
        city_id = city_id,
        name = name,
        age = age,
        email = email,
        password = cls.encrypt_password(password.encode("utf-8")),
        phone = phone,
        cep = cep,
        street = street,
        number_street = number_street,
        complement = complement,
        landmark = landmark,
        district = district
        )
        user.save()

    @staticmethod
    def encrypt_password(password):
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    def save(self):
        db.session.add(self)
        db.session.commit()
        

class UserSchema(ma.Schema):
    city = ma.Nested(city_share_schema)
    roles = ma.Nested(roles_share_schema)
    gender = ma.Nested(gender_share_schema)

    class Meta: 
        fields = ('id', 'gender_id', 'role_id', 'city_id', 'name', 'age', 'email', 'password', 'phone', 'cep' 'street', 'number_street', 'complement', 'landmark', 'district')


user_share_schema = UserSchema()
users_share_schema = UserSchema(many = True)


class UserNewSchema(ma.Schema):
    roles = ma.Nested(roles_share_schema)

    class Meta: 
        fields = ('id', 'role.name', 'name', 'email', 'phone')


user_role_share_schema = UserNewSchema()
users_roles_share_schema = UserNewSchema(many = True)
