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

        if feedback_total != 0:
            five_percentage = round((star_5 * 100) / feedback_total, 2)
            four_percentage = round((star_4 * 100) / feedback_total, 2)
            three_percentage = round((star_3 * 100) / feedback_total, 2)
            two_percentage = round((star_2 * 100) / feedback_total, 2)
            one_percentage = round((star_1 * 100) / feedback_total, 2)
        else:
            five_percentage = 0.0
            four_percentage = 0.0
            three_percentage = 0.0
            two_percentage = 0.0
            one_percentage = 0.0

        dict_feedback = {'five star': star_5, 'four star': star_4, 'three star': star_3, 'two star': star_2,
                         'one star': star_1, 'five-percentage': five_percentage, 'four-percentage': four_percentage,
                         'three-percentage': three_percentage, 'two-percentage': two_percentage,
                         'one-percentage': one_percentage}

        return dict_feedback
