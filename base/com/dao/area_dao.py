from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.city_vo import CityVO
from base.com.vo.state_vo import StateVO


class AreaDAO:
    def insert_area(self, area_vo):
        db.session.add(area_vo)
        db.session.commit()

    def search_area(self):
        area_vo_list = db.session.query(AreaVO, CityVO) \
            .join(CityVO, AreaVO.area_city_id == CityVO.city_id) \
            .all()
        return area_vo_list

    def delete_area(self, area_vo):
        area_vo_list = AreaVO.query.get(area_vo.area_id)
        db.session.delete(area_vo_list)
        db.session.commit()

    def edit_area(self, area_vo):
        area_vo_list = AreaVO.query.get(area_vo.area_id)
        return area_vo_list

    def update_area(self, area_vo):
        db.session.merge(area_vo)
        db.session.commit()

    def view_ajax_city_area(self, city_vo):
        city_vo_list = CityVO.query.filter_by(
            city_state_id=city_vo.city_state_id).all()
        return city_vo_list

    def join_city_data(self, area_vo):
        city_state_list = db.session.query(AreaVO, CityVO, StateVO) \
            .filter(AreaVO.area_id == area_vo.area_id, AreaVO.area_city_id == CityVO.city_id,
                    CityVO.city_state_id == StateVO.state_id).all()
        return city_state_list
