from base import db
from base.com.vo.login_vo import LoginVO


class DatasetVO(db.Model):
    __tablename__ = 'dataset_table'
    dataset_id = db.Column('dataset_id', db.Integer, primary_key=True, autoincrement=True)
    dataset_filename = db.Column('dataset_filename', db.String(255), nullable=False)
    dataset_filepath = db.Column('dataset_filepath', db.String(255), nullable=False)
    dataset_description = db.Column('dataset_description', db.String(255), nullable=False)
    dataset_datetime = db.Column('dataset_datetime', db.DateTime, nullable=False)
    dataset_by = db.Column('dataset_by', db.Integer, db.ForeignKey(LoginVO.login_id, ondelete='CASCADE'))

    def as_dict(self):
        return {
            'dataset_id': self.dataset_id,
            'dataset_name': self.dataset_filename,
            'dataset_filename': self.dataset_filename,
            'dataset_filepath': self.dataset_filepath,
            'dataset_description': self.dataset_description,
            'dataset_datetime': self.dataset_datetime
        }


db.create_all()
