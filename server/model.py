"""
This is the file to declare data models and schemas
"""

from initapp import db, mars

class Business(db.Model):
    """
    Class of business data entry
    """
    bid = db.Column(db.Text, primary_key=True)
    b_name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text)
    rating = db.Column(db.Numeric)
    addr = db.Column(db.Text)
    phone = db.Column(db.Text)
    timestamp = db.Column(db.Text)


class BusinessSchema(mars.SQLAlchemyAutoSchema):
    """
    Schema of Business data entry
    """
    class Meta:
        """
        Declaration of model
        """
        model = Business
