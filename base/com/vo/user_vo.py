from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.city_vo import CityVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.state_vo import StateVO


class UserVO(db.Model):
    __tablename__ = 'user_table'
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    user_organization_name = db.Column('user_organization_name', db.String(255), nullable=False)
    user_contact = db.Column('user_contact', db.String(255), nullable=False)
    user_state_id = db.Column('user_state_id', db.ForeignKey(StateVO.state_id, ondelete='CASCADE'))
    user_city_id = db.Column('user_city_id', db.ForeignKey(CityVO.city_id, ondelete='CASCADE'))
    user_area_id = db.Column('user_area_id', db.ForeignKey(AreaVO.area_id, ondelete='CASCADE'))
    user_address = db.Column('user_address', db.String(255), nullable=False)
    user_fullname = db.Column('user_fullname', db.String(255), nullable=False)
    user_login_id = db.Column('user_login_id', db.ForeignKey(LoginVO.login_id, ondelete='CASCADE'))

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'user_organization_name': self.user_organization_name,
            'user_contact': self.user_contact,
            'user_state_id': self.user_state_id,
            'user_city_id': self.user_city_id,
            'user_area_id': self.user_area_id,
            'user_address': self.user_address,
            'user_fullname': self.user_name,
            'user_login_id': self.user_login_id
        }


db.create_all()
