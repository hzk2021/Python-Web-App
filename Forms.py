from wtforms import Form, StringField, validators, PasswordField, DateField, IntegerField, TextAreaField, SelectField, FileField, RadioField

#region Zhenkai's forms
class CreateEntryForm(Form):
    full_name = StringField('Full Name 👨‍', [validators.Length(min=1, max=30), validators.DataRequired()])
    nric = StringField('NRIC/FIN 🆔', [validators.regexp('^[STFG]\d{7}[A-Z]$', message="Invalid NRIC/FIN"), validators.DataRequired()])
    phone_number = StringField('Phone Number 📱', [validators.Regexp('^[0-9]{8}$', message="Invalid Phone Number"), validators.DataRequired()])
    temperature = StringField('Temperature (°C) 🌡️', [validators.Regexp('\d{2,4}', message="Invalid Temperature (celsius)"), validators.DataRequired()])

class CreateLoginForm(Form):
    username = StringField('Username‍', [validators.Length(min=1, max=30), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class CreateRegisterForm(Form):
    username = StringField('Username‍', [validators.Length(min=1, max=30), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    email = StringField('Email', [validators.Regexp("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", message="Invalid Email!"), validators.DataRequired()])
    phone_number = StringField('Phone Number', [validators.Regexp('^[0-9]{8}$', message="Invalid Phone Number!"),validators.DataRequired()])

class CreateUpdateForm(Form):
    username = StringField('Username‍')
    password = StringField('Password', [validators.DataRequired()])
    email = StringField('Email')
    phone_number = StringField('Phone Number', [validators.Regexp('^[0-9]{8}$', message="Invalid Phone Number!"),validators.DataRequired()])
    points = StringField('Points')

class CreateRewardForm(Form):
    reward_name = StringField('Reward Name‍',[validators.Length(min=1, max=30), validators.DataRequired()])
    points = SelectField('Points', [validators.DataRequired()], choices=[('10', 10), ('20', 20), ('30', 30)])
#endregion

#region Hongray's forms
class CreateSupplierForm(Form):
    name = StringField('Supplier Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    contact_number = StringField('Contact Number', [validators.Regexp('^[0-9]{8}$', message="Invalid Phone Number"), validators.DataRequired()])
    email = StringField('Email Address', [validators.Regexp("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", message="Invalid Email!"), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=1, max=150), validators.DataRequired()])

class CreateOrderForm(Form):
    name = SelectField('Supplier Name', choices=[('default')])
    item = SelectField('Item Details' , choices=[('default')])
    quantity = IntegerField('Quantity Number')

#endregion

#region Limchang's forms

class CreateProduct(Form):
    Image = FileField('image')
    Productname=StringField('Product name',[validators.length(min=1,max=150),validators.data_required(),])
    Productstock = IntegerField('Product in store', validators=[validators.data_required(),validators.NumberRange(1, 100)])
    Productprice = IntegerField('Product price', validators=[validators.data_required()])
    Description = StringField('Specifications', [validators.Length(min=1, max=150), validators.DataRequired()])

#endregion

#region Arief's forms
class Createfeedback(Form):
    name = StringField('Name', [validators.length(min=1, max=150), validators.data_required(), ])
    phone = IntegerField('Phone', validators=[validators.data_required()])
    email = StringField('Email', [validators.Regexp("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"), validators.DataRequired()])
    enquiry = StringField('Remark', [validators.Length(min=1, max=400), validators.DataRequired()])
    service = SelectField('Service', [validators.DataRequired()], choices=['Select', 'Enquiry', 'Product', 'Complaint'])
    status = RadioField('Status', choices=[('pending', 'pending'), ('processed', 'processed')], default='pending')

class Updatefeedback(Form):
    name = StringField('Name', render_kw={'readonly': True})
    phone = IntegerField('Phone', render_kw={'readonly': True})
    email = StringField('Email', render_kw={'readonly': True})
    enquiry = StringField('Remark', render_kw={'readonly': True})
    service = StringField('Service', render_kw={'readonly': True})
    status = RadioField('Status', choices=[('pending', 'pending'), ('processed', 'processed')],default='pending')

#endregion