from base import db
from base.com.vo.dataset_vo import DatasetVO
from base.com.vo.login_vo import LoginVO


class DatasetDAO:
    def insert_dataset(self, dataset_vo):
        db.session.add(dataset_vo)
        db.session.commit()

    def search_datatset(self):
        dataset_vo_list = db.session.query(DatasetVO, LoginVO) \
            .join(LoginVO, DatasetVO.dataset_by == LoginVO.login_id) \
            .all()
        return dataset_vo_list

    def search_dataset_user(self, login_id):
        dataset_vo_list = db.session.query(DatasetVO, LoginVO) \
            .join(LoginVO, DatasetVO.dataset_by == LoginVO.login_id) \
            .filter_by(login_id=login_id) \
            .all()
        return dataset_vo_list

    def delete_dataset(self, dataset_vo):
        dataset_vo_list = DatasetVO.query.get(dataset_vo.dataset_id)
        db.session.delete(dataset_vo_list)
        db.session.commit()
