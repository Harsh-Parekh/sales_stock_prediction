from base import db
from base.com.vo.login_vo import LoginVO


class PasswordotpVO(db.Model):
    __tablename__ = 'password_otp'
    password_otp_id = db.Column('password_otp_id', db.Integer, primary_key=True, autoincrement=True)
    login_id = db.Column('login_id', db.Integer, db.ForeignKey(LoginVO.login_id, ondelete='CASCADE'))
    otp = db.Column('otp', db.String(5), nullable=False)
    time_stamp = db.Column('time_stamp', db.DateTime, nullable=False)

    def as_dict(self):
        return {
            'login_id': self.login_id,
            'otp': self.otp,
            'timestamp': self.time_stamp
        }


db.create_all()
