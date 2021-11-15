from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix="/")

@bp.route('/')
def index():
    return redirect(url_for('question._list')) # .../question/_list 로 routing 되는 view 함수를 찾아감.

