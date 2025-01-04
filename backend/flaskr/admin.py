from functools import wraps

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from db import get_db
bp = Blueprint('admin', __name__, url_prefix='/admin')  # 无urlprefix，因此用于根目录


def user_prev(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return jsonify({
                'success': False,
                'message': '请先登录'
            })
        if g.user['category'] not in ['moderator', 'admin']:
            return jsonify({
                'success': False,
                'message': '权限不足'
            }), 403
        # 如果用户有权限，继续执行视图函数
        return f(*args, **kwargs)
    return decorated_function


def user_prev_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return jsonify({
                'success': False,
                'message': '请先登录'
            })
        if g.user['category'] not in ['admin']:
            return jsonify({
                'success': False,
                'message': '权限不足'
            }), 403
        # 如果用户有权限，继续执行视图函数
        return f(*args, **kwargs)
    return decorated_function


@bp.route("/get_reports", methods=['GET'])
@user_prev_admin
def get_reports():
    db = get_db()
    report_posts = db.execute('''
        SELECT r.*, rr.created, u.username, p.title
        FROM report r
        JOIN report_post rp ON r.report_id = rp.report_id 
        JOIN post p ON p.post_id = rp.post_id
        JOIN release_report rr ON rr.report_id = r.report_id
        JOIN user u ON u.user_id = rr.user_id
    ''').fetchall()
    report_comments = db.execute('''
        SELECT r.*, rr.created, u.username, c.body
        FROM report r
        JOIN report_comment rc ON r.report_id = rc.report_id 
        JOIN comment c ON c.comment_id = rc.comment_id
        JOIN release_report rr ON rr.report_id = r.report_id
        JOIN user u ON u.user_id = rr.user_id
    ''')
    report_post_list = [dict(report_post) for report_post in report_posts]
    report_comment_list = [dict(report_comment) for report_comment in report_comments]
    return jsonify({
        'report_posts': report_post_list,
        'report_comments': report_comment_list
    }), 200


@bp.route('/accept_report<int:report_id>', methods=['POST'])
def accept_report(report_id):
    db = get_db()
    report_post = db.execute('''
        SELECT post_id
        FROM report_post rp
        WHERE rp.report_id = ?
    ''', (report_id, )).fetchone()
    if report_post is not None:
        post_id = report_post[0]
        delete_post(post_id)
        db.execute('''
            UPDATE Report SET report_status = 1 WHERE report_id = ?
        ''', (report_id, ))
        db.commit()
        return jsonify({
            'success': True,
            'message': '审批举报帖子成功，删除帖子成功'
        })
    report_comment = db.execute('''
            SELECT comment_id
            FROM report_comment rc
            WHERE rc.report_id = ?
        ''', (report_id,)).fetchone()
    if report_comment is not None:
        comment_id = report_comment[0]
        delete_comments(comment_id)
        db.execute('''
            UPDATE Report SET report_status = 1 WHERE report_id = ?
        ''', (report_id, ))
        db.commit()
        return jsonify({
            'success': True,
            'message': '审批举报评论成功，删除评论成功'
        })
    return jsonify({
        'success': False,
        'message': '审批举报失败，未找到该举报'
    })


@bp.route('/reject_report<int:report_id>', methods=['POST'])
@user_prev_admin
def reject_report(report_id):
    db = get_db()
    db.execute('''
                UPDATE Report SET report_status = 2 WHERE report_id = ?
            ''', (report_id,))
    db.commit()
    return jsonify({
        'success': True,
        'message': '举报取消成功'
    }), 200

@bp.route('/delete_post<int:post_id>', methods=['POST'])
@user_prev
def delete_post(post_id):
    db = get_db()
    user_id = g.user['user_id']
    post = db.execute('SELECT forum_id FROM post_forum WHERE post_id = ?', (post_id,)).fetchone()
    if post is None:
        return jsonify({
            'success': False,
            'message': '找不到帖子'
        }), 404
    forum_id = post['forum_id']
    if g.user['category'] == 'moderator':
        forum_check = db.execute('SELECT 1 FROM manage_forum WHERE user_id = ? AND forum_id = ?',
                                 (user_id, forum_id)).fetchone()
        if not forum_check:
            return jsonify({
                'success': False,
                'message': '没有权限在该论坛中删除此帖子'
            }), 403
    db.execute('DELETE FROM Post WHERE post_id = ?', (post_id,))
    db.commit()
    db.execute('DELETE FROM release_post WHERE post_id = ?', (post_id,))
    db.commit()
    db.execute('DELETE FROM post_forum WHERE post_id = ?', (post_id,))
    db.commit()
    return jsonify({
        "success": True,
        "message": "删除帖子成功"
    }), 200


@bp.route('/delete_comment<int:comment_id>', methods=['POST'])
@user_prev_admin
def delete_comments(comment_id):
    print(comment_id)
    db = get_db()
    db.execute('''
                DELETE FROM Comment WHERE comment_id = ? 
            ''', (comment_id,))
    db.commit()
    db.execute('''
        DELETE FROM release_comment WHERE comment_id = ?
    ''', (comment_id,))
    db.commit()
    db.execute('''
        DELETE FROM com_post WHERE comment_id = ?
    ''', (comment_id,))
    db.commit()
    db.execute('''
            DELETE FROM parent WHERE parent_comment_id = ?
        ''', (comment_id,))
    db.commit()
    return jsonify({
        "success": True,
        "message": "删除帖子成功"
    }), 200


@bp.route('/get_applies', methods=['GET'])
@user_prev_admin
def get_applies():
    db = get_db()
    applies = db.execute('''
        SELECT a.*, u.username, ua.created_at
        FROM Apply a
        JOIN user_apply ua ON ua.apply_id = a.apply_id
        JOIN user u ON u.user_id = ua.user_id
    ''').fetchall()
    apply_list = [dict(apply) for apply in applies]
    return jsonify(apply_list)


@bp.route("/accept_apply<int:apply_id>", methods=['POST'])
@user_prev_admin
def accept_apply(apply_id):
    db = get_db()
    count = db.execute('''
        SELECT COUNT(*) FROM Forum
    ''').fetchone()[0]
    if count >= 10:
        return jsonify({
            'success': False,
            'message': '论坛数量超过上限'
        })
    forum_name = request.get_json().get('forum_name')
    description = request.get_json().get('description')
    db.execute('''
        INSERT INTO Forum (forum_name, description) VALUES (?,?)
    ''', (forum_name, description, ))
    db.commit()
    db.execute('''
        UPDATE Apply SET apply_status = 1 WHERE apply_id = ?
    ''', (apply_id, ))
    db.commit()
    return jsonify({
        'success': True,
        'message': '创建论坛成功'
    }), 200


@bp.route("/reject_apply<int:apply_id>", methods=['POST'])
@user_prev_admin
def reject_apply(apply_id):
    db = get_db()
    db.execute('''
            UPDATE Apply SET apply_status = 2 WHERE apply_id = ?
        ''', (apply_id,))
    db.commit()
    return jsonify({
        'success': True,
        'message': '申请取消成功'
    }), 200


@bp.route('/get_users', methods=['GET'])
@user_prev_admin
def get_users():
    db = get_db()
    users = db.execute('''
        SELECT * FROM user
    ''').fetchall()
    user_list = [dict(user) for user in users]
    return jsonify(user_list)


@bp.route('/delete_user<int:user_id>', methods=['POST'])
@user_prev_admin
def delete_user(user_id):
    db = get_db()
    db.execute('''
        DELETE FROM USER WHERE user_id = ? 
    ''', (user_id, ))
    db.commit()
    return jsonify({
        'success': True,
        'message': '删除用户成功'
    })


@bp.route('/get_posts', methods=['GET'])
@user_prev_admin
def get_posts():
    db = get_db()
    posts = db.execute('''
        SELECT p.*, u.username, f.forum_name, rp.created
        FROM Post p
        JOIN release_post rp ON rp.post_id = p.post_id
        JOIN user u ON u.user_id = rp.post_id
        JOIN post_forum pf ON pf.post_id = p.post_id
        JOIN forum f ON f.forum_id = pf.forum_id 
    ''').fetchall()
    post_list = [dict(post) for post in posts]
    return jsonify(post_list)


@bp.route('/get_comments', methods=['GET'])
@user_prev_admin
def get_comments():
    db = get_db()
    comments = db.execute('''
        SELECT c.*, u.username, p.title, rc.created_at
        FROM Comment c
        JOIN release_comment rc ON rc.comment_id = c.comment_id
        JOIN user u ON u.user_id = rc.comment_id
        JOIN com_post cp ON cp.comment_id = c.comment_id
        JOIN post p ON p.post_id = cp.post_id 
    ''').fetchall()
    comment_list = [dict(comment) for comment in comments]
    return jsonify(comment_list)
