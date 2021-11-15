from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .. import db
from .. forms import UserCreateForm, UserLoginForm
from .. models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None   # ??????
        user = User.query.filter_by(username=form.username.data).first()
        # print(user)  # <User 1>
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다. "
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request # 다른 route 함수들 보다 먼저 실행되도록 만드는 이너테이션 (flask 기본 제공)
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
        # g: 글로벌 변수(Application Context영역), 방문자수 등 모든 사용자와 공유되어야 하는 변수??
        # 웹 애플리케이션은 context라는 것을 가짐
        # 애플리케이션이 실행 될때는 어떠한 영역을 가짐
        # 그중에는 애플리케이션 컨텍스트라는 영역과 비교되는 세션 컨텍스트라는 영역이 존재
        # 세션 컨텍스트는 해당 웹 애플리케이션으로 들어오는 하나의! 브러우저로 부터 들어오는 요청을 뜻함
        # 애플리케이션 컨텍스트는 해당 웹 애플리케이션으로 들어오는 모든 불특정 다수의 브라우저 요청을 뜻함
        # 이중 g라는 것은 애플리케이션 컨텍스트의 영역임
        # 애플리케이션 컨텍스트 = 모든 사용자가 공유
        # 세션 컨텍스트 = 한명의 사용자만 공유 ( 로그인정보 )

        """
        load_logged_in_user 함수에서 사용한 g는 플라스크가 제공하는 컨텍스트 변수이다.
        이 변수는 request 변수와 마찬가지로[요청 → 응답] 과정에서 유효하다.
        코드에서 보듯 session 변수에 user_id값이 있으면 데이터베이스에서 이를 조회하여 g.user 에 저장한다
        
        이렇게 하면 이후 사용자 로그인 검사를 할 때, session 을 조사할 필요가 없다. g.user 에 값이 있는지만 알아내면 된다. 
        g.user 에는 User 객체가 저장되어 있으므로 여려 가지 사용자 정보 (username, email 등) 을 추가로 얻어내는 이점이 있다. 
        
        # g.user에는 User 객체가 저장된다.
        """
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view