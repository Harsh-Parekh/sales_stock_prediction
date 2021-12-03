from base import db
from base.com.vo.login_vo import LoginVO


class LoginDAO:
    def find_login_id(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_username=login_vo.login_username).all()
        return login_vo_list[0].login_id

    def find_login_username(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_id=login_vo.login_id).all()
        return login_vo_list[0].login_username

    def insert_login(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()

    def validate_login(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_username=login_vo.login_username,
                                                login_password=login_vo.login_password)
        return login_vo_list

    def get_login_data(self, login_secretkey):
        login_vo_list = LoginVO.query.filter_by(login_secretkey=login_secretkey).all()
        return login_vo_list[0]

    def is_exist(self, login_vo):
        login_vo_exist = LoginVO.query.filter_by(login_username=login_vo.login_username).all()
        if len(login_vo_exist) == 0:
            return True
        else:
            return False

    def update_password(self, login_vo):
        LoginVO.query.filter_by(login_username=login_vo.login_username).update(
            dict(login_password=login_vo.login_password))
        db.session.commit()

    def users(self):
        user_list_active = len(LoginVO.query.filter_by(login_status='active').all()) - 1
        total_user = len(db.session.query(LoginVO).all()) - 1
        active, block = user_list_active, total_user - user_list_active

        if total_user == 0:
            percentage = 0.0
            return percentage, total_user, active, block

        percentage = round((user_list_active * 100 / total_user), 2)
        return percentage, total_user, active, block
