from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField # EmailField
#from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])  # '제목' : form label 로
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')]) # 오류 메세지를 한글
    # validators : 검증을 위해 사용되는 도구로 필수 항목인지를 체크하는 DataRequired,
    #              이메일인지를 체크하는 Email, 길이를 체크하는 length emd
    # 사용 예     : validators=[DataRequired(), Email()]

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])