"""
User authentication module for Cloud Cost Optimizer.
This module provides user registration, login, and session management.
"""

import os
import json
import logging
import uuid
import hashlib
import secrets
import datetime
import functools
from typing import Dict, Any, Optional, List
import jwt
from flask import Blueprint, request, jsonify, current_app, g

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

# In-memory user store for development (would use database in production)
# This is just for demonstration - in a real app, use a proper database
users_db = {}
sessions = {}

@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'full_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']
    full_name = data['full_name']
    
    # Check if username or email already exists
    for user_id, user in users_db.items():
        if user['username'] == username:
            return jsonify({'error': 'Username already exists'}), 409
        if user['email'] == email:
            return jsonify({'error': 'Email already exists'}), 409
    
    # Hash password
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    
    # Create user
    user_id = str(uuid.uuid4())
    user = {
        'id': user_id,
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'salt': salt,
        'full_name': full_name,
        'role': 'user',  # Default role
        'created_at': datetime.datetime.now().isoformat(),
        'last_login': None
    }
    
    # Store user
    users_db[user_id] = user
    
    # Return user info (without sensitive data)
    user_info = {
        'id': user_id,
        'username': username,
        'email': email,
        'full_name': full_name,
        'role': 'user'
    }
    
    return jsonify(user_info), 201

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.get_json()
    
    # Validate required fields
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    
    username = data['username']
    password = data['password']
    
    # Find user by username
    user = None
    for user_id, user_data in users_db.items():
        if user_data['username'] == username:
            user = user_data
            break
    
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Verify password
    password_hash = hashlib.sha256((password + user['salt']).encode()).hexdigest()
    if password_hash != user['password_hash']:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Generate JWT token
    secret_key = os.environ.get('JWT_SECRET_KEY', 'development_secret_key')
    expiration = datetime.datetime.now() + datetime.timedelta(hours=24)
    
    payload = {
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': expiration
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    # Update last login
    user['last_login'] = datetime.datetime.now().isoformat()
    
    # Create session
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        'user_id': user['id'],
        'created_at': datetime.datetime.now().isoformat(),
        'expires_at': expiration.isoformat()
    }
    
    # Return token and user info
    response = {
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user['role']
        }
    }
    
    return jsonify(response), 200

@auth_bp.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    """Logout a user."""
    # In a stateless JWT setup, the client simply discards the token
    # For added security, we could implement a token blacklist
    
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Logged out successfully'}), 200
    
    token = auth_header.split(' ')[1]
    
    # In a real implementation, add the token to a blacklist
    # For this demo, we'll just return success
    
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/api/v1/auth/me', methods=['GET'])
def get_current_user():
    """Get the current user's information."""
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # Decode the token
        secret_key = os.environ.get('JWT_SECRET_KEY', 'development_secret_key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Get user from database
        user_id = payload['user_id']
        if user_id not in users_db:
            return jsonify({'error': 'User not found'}), 404
        
        user = users_db[user_id]
        
        # Return user info
        user_info = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user['role']
        }
        
        return jsonify(user_info), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@auth_bp.route('/api/v1/auth/users', methods=['GET'])
def get_users():
    """Get all users (admin only)."""
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # Decode the token
        secret_key = os.environ.get('JWT_SECRET_KEY', 'development_secret_key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Check if user is admin
        if payload.get('role') != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        
        # Return all users (without sensitive data)
        user_list = []
        for user_id, user in users_db.items():
            user_list.append({
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role'],
                'created_at': user['created_at'],
                'last_login': user['last_login']
            })
        
        return jsonify(user_list), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

# Authentication middleware
@auth_bp.before_app_request
def authenticate_request():
    """Authenticate the request and set the current user."""
    # Skip authentication for login and register routes
    if request.path in ['/api/v1/auth/login', '/api/v1/auth/register']:
        return
    
    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        g.current_user = None
        return
    
    token = auth_header.split(' ')[1]
    
    try:
        # Decode the token
        secret_key = os.environ.get('JWT_SECRET_KEY', 'development_secret_key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Get user from database
        user_id = payload['user_id']
        if user_id in users_db:
            g.current_user = users_db[user_id]
        else:
            g.current_user = None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        g.current_user = None

# Helper functions
def require_auth(f):
    """Decorator to require authentication."""
    @functools.wraps(f)  # Preserve function name and docstring
    def decorated(*args, **kwargs):
        if not g.current_user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

def require_admin(f):
    """Decorator to require admin privileges."""
    @functools.wraps(f)  # Preserve function name and docstring
    def decorated(*args, **kwargs):
        if not g.current_user:
            return jsonify({'error': 'Authentication required'}), 401
        if g.current_user.get('role') != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated

# Create an admin user for testing
admin_id = str(uuid.uuid4())
admin_salt = secrets.token_hex(16)
admin_password_hash = hashlib.sha256(('admin' + admin_salt).encode()).hexdigest()

users_db[admin_id] = {
    'id': admin_id,
    'username': 'admin',
    'email': 'admin@example.com',
    'password_hash': admin_password_hash,
    'salt': admin_salt,
    'full_name': 'Admin User',
    'role': 'admin',
    'created_at': datetime.datetime.now().isoformat(),
    'last_login': None
}
