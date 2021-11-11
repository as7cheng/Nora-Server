"""
This is the file to declare data models and schemas
"""

from initapp import DB, MA

class Business(DB.Model):
    """
    Class of business data entry
    """
    bid = DB.Column(DB.Text, primary_key=True)
    b_name = DB.Column(DB.Text, nullable=False)
    url = DB.Column(DB.Text)
    rating = DB.Column(DB.Numeric)
    addr = DB.Column(DB.Text)
    phone = DB.Column(DB.Text)
    timestamp = DB.Column(DB.Text)


class BusinessSchema(MA.SQLAlchemyAutoSchema):
    """
    Schema of Business data entry
    """
    class Meta:
        """
        Declaration of model
        """
        model = Business
