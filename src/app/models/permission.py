from src.app import db, ma


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    description = db.Column(db.String(84), nullable = False)

    def __init__(self, description):
        self.description = description

    @classmethod
    def seed(cls, description):
        permission = Permission(
        description = description
        )
        permission.save()

    def save(self):
        db.session.add(self)
        db.session.commit()


class PermissionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')
    
    
permission_share_schema = PermissionSchema()
permissions_share_schema = PermissionSchema(many = True)
