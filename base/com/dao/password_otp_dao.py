from base import db
from base.com.vo.password_otp_vo import PasswordotpVO
from datetime import datetime


class PasswordotpDAO:
    def insert_passwordotp(self, password_otp_vo):
        db.session.add(password_otp_vo)
        db.session.commit()

    def validate(self, password_vo):
        password_vo_list = PasswordotpVO.query.filter_by(
            login_id=password_vo.login_id, otp=password_vo.otp
        ).all()
        if len(password_vo_list) > 0:
            current = datetime.strptime(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "%Y-%m-%d %H:%M:%S",
            )
            time_stamp = datetime.strptime(
                str(password_vo_list[0].time_stamp), "%Y-%m-%d %H:%M:%S"
            )
            if (current - time_stamp).seconds < 300:
                password_vo_list_delete = PasswordotpVO.query.get(
                    password_vo_list[0].password_otp_id
                )
                db.session.delete(password_vo_list_delete)
                return True
            else:
                return False
        else:
            return "invalid credentials"
