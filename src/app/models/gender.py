from src.app import db, ma


class Gender(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    description = db.Column(db.String(84), nullable = False)

    def __init__(self, description):
        self.description = description
        
    @classmethod
    def seed(cls, description):
        gender = Gender(
        description = description
        )
        gender.save()

    def save(self): 
        db.session.add(self)
        db.session.commit()


class GenderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')


gender_share_schema = GenderSchema()
genders_share_schema = GenderSchema(many = True)
