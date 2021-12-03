from base import db
from base.com.vo.login_vo import LoginVO


class PredictionVO(db.Model):
    __tablename__ = "prediction_table"
    prediction_id = db.Column('prediction_id', db.Integer, primary_key=True, autoincrement=True)
    prediction_no_stock_purchased = db.Column('prediction_no_stock_purchased', db.Integer, nullable=False)
    prediction_no_stock_returned = db.Column('prediction_no_stock_returned', db.Integer, nullable=False)
    prediction_no_stock_remains = db.Column('prediction_no_stock_remains', db.Integer, nullable=False)
    prediction_stock_type = db.Column('prediction_stock_type', db.String(100), nullable=False)
    prediction_stock_purchased_season = db.Column('prediction_stock_purchased_season', db.String(100), nullable=False)
    prediction_stock_sell_season = db.Column('prediction_stock_sell_season', db.String(100), nullable=False)
    prediction_stock_purchased_month = db.Column('prediction_stock_purchased_month', db.String(100), nullable=False)
    prediction_stock_sell_duration_months = db.Column('prediction_stock_sell_duration_months', db.Integer,
                                                      nullable=False)
    prediction_year = db.Column('prediction_Year', db.Integer)
    prediction_no_stock_sell = db.Column('prediction_no_stock_sell', db.Integer, nullable=False)
    prediction_datetime = db.Column('prediction_datetime', db.DateTime, nullable=False)
    prediction_login_id = db.Column('prediction_login_id', db.ForeignKey(LoginVO.login_id, ondelete='CASCADE'))

    def as_dict(self):
        return {
            'prediction_id': self.prediction_id,
            'prediction_no_stock_purchased': self.prediction_no_stock_purchased,
            'prediction_no_stock_returned': self.prediction_no_stock_returned,
            'prediction_no_stock_remains': self.prediction_no_stock_remains,
            'prediction_stock_type': self.prediction_stock_type,
            'prediction_stock_purchased_season': self.prediction_stock_purchased_season,
            'prediction_stock_sell_season': self.prediction_stock_sell_season,
            'prediction_stock_purchased_month': self.prediction_stock_purchased_month,
            'prediction_stock_sell_duration_months': self.prediction_stock_sell_duration_months,
            'prediction_year': self.prediction_year,
            'prediction_no_stock_sell': self.prediction_no_stock_sell
        }


db.create_all()
