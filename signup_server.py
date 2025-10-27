#!/usr/bin/env python3
"""
Newsletter Signup Web Server
Simple web interface for newsletter subscription management
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for
from email_manager import EmailManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Initialize email manager
email_manager = EmailManager()

@app.route('/')
def index():
    """Main signup page"""
    stats = email_manager.get_stats()
    return render_template('signup.html', stats=stats)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Handle newsletter subscription"""
    try:
        data = request.get_json() if request.is_json else request.form
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        result = email_manager.subscribe(email, name)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Subscription error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during subscription'
        }), 500

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    """Handle newsletter unsubscription"""
    try:
        if request.method == 'GET':
            # Show unsubscribe form
            email = request.args.get('email', '')
            token = request.args.get('token', '')
            return render_template('unsubscribe.html', email=email, token=token)
        
        # Handle POST request
        data = request.get_json() if request.is_json else request.form
        email = data.get('email', '').strip()
        token = data.get('token', '').strip()
        
        if not email and not token:
            return jsonify({
                'success': False,
                'message': 'Email or unsubscribe token is required'
            }), 400
        
        result = email_manager.unsubscribe(email, token)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Unsubscription error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during unsubscription'
        }), 500

@app.route('/admin')
def admin():
    """Admin panel for managing subscribers"""
    try:
        subscribers = email_manager.get_all_subscribers()
        stats = email_manager.get_stats()
        return render_template('admin.html', subscribers=subscribers, stats=stats)
    except Exception as e:
        logger.error(f"Admin panel error: {e}")
        return f"Error loading admin panel: {e}", 500

@app.route('/api/subscribers')
def api_subscribers():
    """API endpoint to get subscribers"""
    try:
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        subscribers = email_manager.export_subscribers(include_inactive)
        return jsonify({
            'success': True,
            'subscribers': subscribers,
            'count': len(subscribers)
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching subscribers'
        }), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint to get subscription statistics"""
    try:
        stats = email_manager.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Stats API error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching statistics'
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting newsletter signup server on port {port}")
    print(f"📧 Admin panel: http://localhost:{port}/admin")
    print(f"📊 API stats: http://localhost:{port}/api/stats")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
