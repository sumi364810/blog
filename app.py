from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flaskアプリケーションの初期化
app = Flask(__name__)

# データベース設定 (SQLiteをプロジェクトフォルダ内に作成)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 記事のデータベースモデル
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.id}>'

# データベースファイルの作成
with app.app_context():
    db.create_all()

# ルート (URLと関数のマッピング)

# ブログ一覧ページ
@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

# 記事投稿・編集ページ (GET: フォーム表示, POST: 記事作成/更新)
@app.route('/post', methods=['GET', 'POST'])
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_article(post_id=None):
    post = None
    if post_id:
        post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if post_id:
            # 更新処理
            post.title = title
            post.content = content
        else:
            # 新規作成処理
            new_post = Post(title=title, content=content)
            db.session.add(new_post)

        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('post.html', post=post)

# 記事削除
@app.route('/delete/<int:post_id>')
def delete_article(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return '記事の削除中にエラーが発生しました'

if __name__ == '__main__':
    # デバッグモードで実行 (開発時のみ)
    app.run(debug=True)