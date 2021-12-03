from base import db
from base.com.vo.state_vo import StateVO


class StateDAO:
    def insert_state(self, state_vo):
        db.session.add(state_vo)
        db.session.commit()

    def search_state(self):
        state_vo_list = db.session.query(StateVO).all()
        return state_vo_list

    def delete_state(self, state_vo):
        state_vo_list = StateVO.query.get(state_vo.state_id)
        db.session.delete(state_vo_list)
        db.session.commit()

    def edit_state(self, state_vo):
        state_vo_list = StateVO.query.get(state_vo.state_id)
        return state_vo_list

    def update_state(self, state_vo):
        db.session.merge(state_vo)
        db.session.commit()
