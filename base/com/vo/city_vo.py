from base import db
from base.com.vo.state_vo import StateVO


class CityVO(db.Model):
    __tablename__ = 'city_table'
    city_id = db.Column('city_id', db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column('city_name', db.String(255), nullable=False)
    city_description = db.Column('city_description', db.String(255), nullable=False)
    city_state_id = db.Column('city_state_id', db.Integer,
                              db.ForeignKey(StateVO.state_id, ondelete='CASCADE'))

    def as_dict(self):
        return {
            'city_id': self.city_id,
            'city_name': self.city_name,
            'city_description': self.city_description,
            'city_state_id': self.city_state_id
        }


db.create_all()
