"""
File to declare data models and schemas
"""

from initapp import DB, MA

class Business(DB.Model):
    """
    Class of business data entry
    """
    id = DB.Column(DB.Text, primary_key=True)
    name = DB.Column(DB.Text, nullable=False)
    image = DB.Column(DB.Text)
    url = DB.Column(DB.Text)
    tags = DB.Column(DB.ARRAY(DB.Text))
    rating = DB.Column(DB.Numeric)
    transaction = DB.Column(DB.ARRAY(DB.Text))
    price = DB.Column(DB.Text)
    addr = DB.Column(DB.Text)
    city = DB.Column(DB.Text)
    state = DB.Column(DB.Text)
    zip_code = DB.Column(DB.Text)
    phone = DB.Column(DB.Text)
    timestamp = DB.Column(DB.Text)
    metropolitan = DB.Column(DB.Text)
    term = DB.Column(DB.Text)
    city_population = DB.Column(DB.Text)

class BusinessSchema(MA.SQLAlchemyAutoSchema):
    """
    Schema of Business data entry
    """
    class Meta:
        """
        Declaration of model
        """
        model = Business
