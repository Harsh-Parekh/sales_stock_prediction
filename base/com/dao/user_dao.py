from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.city_vo import CityVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.state_vo import StateVO
from base.com.vo.user_vo import UserVO


class UserDAO:
    def view_ajax_city(self, city_vo):
        city_vo_list = CityVO.query.filter_by(
            city_state_id=city_vo.city_state_id).all()
        return city_vo_list

    def view_ajax_area(self, area_vo):
        area_vo_list = AreaVO.query.filter_by(
            area_city_id=area_vo.area_city_id).all()
        return area_vo_list

    def insert_user(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()

    def search_user(self):
        user_vo_list = db.session.query(UserVO, StateVO, CityVO, AreaVO, LoginVO) \
            .join(StateVO, UserVO.user_state_id == StateVO.state_id) \
            .join(CityVO, UserVO.user_city_id == CityVO.city_id) \
            .join(AreaVO, UserVO.user_area_id == AreaVO.area_id) \
            .join(LoginVO, UserVO.user_login_id == LoginVO.login_id) \
            .all()
        return user_vo_list

    def get_user(self, login_id):
        user_vo = db.session.query(LoginVO, UserVO).join(UserVO).filter_by(user_login_id=login_id).all()
        return user_vo[0]

    def user_block_unblock(self, login_vo):
        login_id = login_vo.login_id
        login_vo = LoginVO.query.filter_by(login_id=login_id).first()
        if login_vo.login_status == 'active':
            login_vo.login_status = 'inactive'
            db.session.commit()
        elif login_vo.login_status == 'inactive':
            login_vo.login_status = 'active'
            db.session.commit()

    def update_login_profile(self, login_vo_old):
        login_id = login_vo_old.login_id
        login_vo = LoginVO.query.filter_by(login_id=login_id).first()
        login_vo.login_username = login_vo_old.login_username
        login_vo.login_password = login_vo_old.login_password
        db.session.commit()

    def update_user_profile(self, user_vo):
        db.session.merge(user_vo)
        db.session.commit()
