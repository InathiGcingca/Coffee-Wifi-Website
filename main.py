from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,URL
import csv
import ftfy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location on Google Maps(URL)', validators=[DataRequired(),URL()])
    open_time = StringField(label='Opening Time e.g 8AM',validators=[DataRequired()])
    close_time = StringField(label='Closing Time e.g 5;30PM', validators=[DataRequired()])
    coffee = SelectField(u'Coffee Rating', choices=(['✘','☕️','☕️☕️','☕️☕️☕️','☕️☕️☕️☕️','☕️☕️☕️☕️☕'])
                         ,validators=[DataRequired()])
    wifi = SelectField(u'Wifi Strength Rating',choices=(['✘','💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'])
                       ,validators=[DataRequired()])
    power = SelectField(u'Power Socket Availability',choices=(['✘','🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'])
                       ,validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv",mode='a',encoding="utf-8") as file:
             file.write(f"\n{form.cafe.data},{form.location.data},{form.open_time.data},"
                        f"{form.close_time.data},{form.coffee.data},{form.wifi.data},"
                        f"{form.power.data}")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv',newline='',encoding='unicode-escape') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            new_row = [ftfy.fix_text(item) for item in row]
            list_of_rows.append(new_row)
        length = len(list_of_rows[1])
        num_cafes = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, length=length,index=0,position=num_cafes)


if __name__ == '__main__':
    app.run(debug=True)
