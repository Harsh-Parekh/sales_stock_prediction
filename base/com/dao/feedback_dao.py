from base import db
from base.com.vo.feedback_vo import FeedbackVO
from base.com.vo.login_vo import LoginVO


class FeedbackDAO:
    def insert_feedback(self, feedback_vo):
        db.session.add(feedback_vo)
        db.session.commit()

    def user_feedback_list(self, user_id):
        user_feedback = db.session.query(FeedbackVO, LoginVO) \
            .join(LoginVO, FeedbackVO.feedback_login_id == LoginVO.login_id) \
            .all()
        return user_feedback

    def admin_feeback_list(self):
        feedback_vo_list = db.session.query(FeedbackVO, LoginVO) \
            .join(LoginVO, FeedbackVO.feedback_login_id == LoginVO.login_id) \
            .all()
        return feedback_vo_list

    def delete_feedback(self, feedback_vo):
        feedback_vo_list = FeedbackVO.query.get(feedback_vo.feedback_id)
        db.session.delete(feedback_vo_list)
        db.session.commit()

    def feedback_data(self):
        feedback_total = len(db.session.query(FeedbackVO).all())
        star_1 = len(FeedbackVO.query.filter_by(feedback_rating=1).all())
        star_2 = len(FeedbackVO.query.filter_by(feedback_rating=2).all())
        star_3 = len(FeedbackVO.query.filter_by(feedback_rating=3).all())
        star_4 = len(FeedbackVO.query.filter_by(feedback_rating=4).all())
        star_5 = len(FeedbackVO.query.filter_by(feedback_rating=5).all())

        fivepercentage = round((star_5 * 100) / feedback_total, 2)
        fourpercentage = round((star_4 * 100) / feedback_total, 2)
        threepercentage = round((star_3 * 100) / feedback_total, 2)
        twopercentage = round((star_2 * 100) / feedback_total, 2)
        onepercentage = round((star_1 * 100) / feedback_total, 2)

        dict_feedback = {'fivestar': star_5, 'fourstar': star_4, 'threestar': star_3, 'twostar': star_2,
                         'onestar': star_1, 'fivepercentage': fivepercentage, 'fourpercentage': fourpercentage,
                         'threepercentage': threepercentage, 'twopercentage': twopercentage,
                         'onepercentage': onepercentage}
        return dict_feedback
