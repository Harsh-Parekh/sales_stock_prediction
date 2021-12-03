from base import db


class StateVO(db.Model):
    __tablename__ = 'state_table'
    state_id = db.Column('state_id', db.Integer, primary_key=True, autoincrement=True)
    state_name = db.Column('state_name', db.String(255), nullable=False)
    state_description = db.Column('state_description', db.String(255), nullable=False)

    def as_dict(self):
        return {
            'state_id': self.state_id,
            'state_name': self.state_name,
            'state_description': self.state_description
        }


db.create_all()
