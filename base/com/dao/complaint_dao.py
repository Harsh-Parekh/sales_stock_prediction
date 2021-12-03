from base import db
from base.com.vo.complaint_vo import ComplaintVO
from base.com.vo.login_vo import LoginVO


class ComplaintDAO:
    def insert_complaint(self, complaint_vo):
        db.session.add(complaint_vo)
        db.session.commit()

    def user_complaint_list(self, user_id):
        user_complaint = db.session.query(ComplaintVO, LoginVO) \
            .join(LoginVO, ComplaintVO.complaint_from_login_id == LoginVO.login_id) \
            .filter_by(login_id=user_id) \
            .all()
        return user_complaint

    def admin_complaint_list(self):
        complaint_vo_list = db.session.query(ComplaintVO, LoginVO) \
            .join(LoginVO, ComplaintVO.complaint_from_login_id == LoginVO.login_id) \
            .all()
        return complaint_vo_list

    def delete_complaint(self, complaint_vo):
        complaint_vo_list = ComplaintVO.query.get(complaint_vo.complaint_id)
        db.session.delete(complaint_vo_list)
        db.session.commit()

    def get_complaint(self, complaint_vo):
        complaint_vo_list = ComplaintVO.query.get(complaint_vo.complaint_id)
        return complaint_vo_list

    def insert_replied_complaint(self, complaint_vo):
        db.session.merge(complaint_vo)
        db.session.commit()

    def complaint_pending(self):
        total_complaint = len(db.session.query(ComplaintVO).all())
        complaint_list_pending = len(ComplaintVO.query.filter_by(complaint_status='pending').all())
        percentage = round((complaint_list_pending * 100) / total_complaint, 2)
        return (percentage, complaint_list_pending)
