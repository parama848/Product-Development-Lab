# from flask import Flask, request, jsonify, render_template, send_file
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# import pandas as pd
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Comment Model
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     text = db.Column(db.String(500), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# # Save to Excel Function
# def save_to_excel():
#     comments = Comment.query.order_by(Comment.timestamp.desc()).all()
#     data = [{'Name': c.name, 'Comment': c.text, 'Timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for c in comments]
#     df = pd.DataFrame(data)
#     df.to_excel('comments.xlsx', index=False)

# # Serve the frontend page
# @app.route('/')
# def index():
#     return render_template('feedback.html')

# # Fetch all comments
# @app.route('/comments', methods=['GET'])
# def get_comments():
#     comments = Comment.query.order_by(Comment.timestamp.desc()).all()
#     return jsonify([{'name': c.name, 'text': c.text, 'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for c in comments])

# # Add a comment
# @app.route('/comments', methods=['POST'])
# def add_comment():
#     data = request.get_json()
#     new_comment = Comment(name=data['name'], text=data['text'])
#     db.session.add(new_comment)
#     db.session.commit()
#     save_to_excel()
#     return jsonify({'message': 'Comment added successfully!'}), 201

# # Download Excel file
# @app.route('/download_excel', methods=['GET'])
# def download_excel():
#     return send_file('comments.xlsx', as_attachment=True)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         if not os.path.exists('comments.xlsx'):
#             save_to_excel()
#     app.run(debug=True)



from flask import Flask, request, jsonify, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Save to Excel Function
def save_to_excel():
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    data = [{'ID': c.id, 'Name': c.name, 'Comment': c.text, 'Timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for c in comments]
    df = pd.DataFrame(data)
    df.to_excel('comments.xlsx', index=False)

# Serve the frontend page
@app.route('/')
def index():
    return render_template('feedback.html')

# Fetch all comments
@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return jsonify([
        {'id': c.id, 'name': c.name, 'text': c.text, 'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        for c in comments
    ])

# Add a comment
@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    new_comment = Comment(name=data['name'], text=data['text'])
    db.session.add(new_comment)
    db.session.commit()
    save_to_excel()
    return jsonify({'message': 'Comment added successfully!'}), 201

# Delete a comment
@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        return jsonify({'error': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()
    save_to_excel()
    
    return jsonify({'message': 'Comment deleted successfully!'}), 200

# Download Excel file
@app.route('/download_excel', methods=['GET'])
def download_excel():
    return send_file('comments.xlsx', as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not os.path.exists('comments.xlsx'):
            save_to_excel()
    app.run(debug=True)

