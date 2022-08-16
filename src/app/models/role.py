from src.app import db, ma
from src.app.models.permission import permissions_share_schema


role_permissions = db.Table('role_permissions',
                    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
                    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
                    )


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    description = db.Column(db.String(200), nullable = False)
    name = db.Column(db.String(84), nullable = False)
    permissions = db.relationship('Permission', secondary=role_permissions, backref='roles')

    def __init__(self, description, name, permissions):
        self.description = description
        self.name = name
        self.permissions = permissions

    @classmethod
    def seed(cls, description, name, permissions):
        role = Role(
            description = description,
            name = name,
            permissions = permissions
        )
        role.save()

    def save(self):
        db.session.add(self)
        db.session.commit()


class RoleSchema(ma.Schema):
    permissions = ma.Nested(permissions_share_schema)
    class Meta:
        fields = ('id', 'description', 'name', 'permissions')


role_share_schema = RoleSchema()
roles_share_schema = RoleSchema(many = True)
