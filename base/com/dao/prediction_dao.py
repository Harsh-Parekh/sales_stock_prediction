from base import db
from base.com.vo.prediction_vo import PredictionVO
from base.com.vo.login_vo import LoginVO


class PredictionDAO:
    def insert_prediction(self, prediction_vo):
        db.session.add(prediction_vo)
        db.session.commit()

    def search_prediction(self):
        prediction_vo_list = db.session.query(PredictionVO, LoginVO) \
            .join(LoginVO, PredictionVO.prediction_login_id == LoginVO.login_id) \
            .all()
        return prediction_vo_list

    def user_prediction(self, user_id):
        prediction_vo_list = PredictionVO.query.filter_by(prediction_login_id=user_id).all()
        return prediction_vo_list

    def previous_prediction(self, prediction_vo):
        prediction_vo_data = PredictionVO.query.get(prediction_vo.prediction_id)
        return prediction_vo_data

    def total_prediction(self):
        total_prediction = len(db.session.query(PredictionVO).all())
        return total_prediction
