"""
Database Manager Module
Handles all database operations for user management and prediction history
"""

import sqlite3
import bcrypt
from datetime import datetime
from pathlib import Path
import config

class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self):
        """Initialize database connection"""
        self.db_path = config.DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                age INTEGER,
                gender TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                disease_type TEXT NOT NULL,
                prediction_result INTEGER NOT NULL,
                risk_probability REAL NOT NULL,
                risk_level TEXT NOT NULL,
                input_parameters TEXT,
                prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password, full_name=None, age=None, gender=None):
        """
        Create a new user
        Returns: (success: bool, message: str, user_id: int or None)
        """
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, age, gender)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, age, gender))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, "Account created successfully!", user_id
            
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return False, "Username already exists!", None
            elif 'email' in str(e):
                return False, "Email already exists!", None
            else:
                return False, "Error creating account!", None
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def authenticate_user(self, username, password):
        """
        Authenticate user
        Returns: (success: bool, message: str, user_data: dict or None)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            conn.close()
            
            if user is None:
                return False, "Username not found!", None
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                user_data = {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'age': user['age'],
                    'gender': user['gender']
                }
                return True, "Login successful!", user_data
            else:
                return False, "Incorrect password!", None
                
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'age': user['age'],
                    'gender': user['gender'],
                    'created_at': user['created_at']
                }
            return None
            
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def save_prediction(self, user_id, disease_type, prediction_result, 
                       risk_probability, risk_level, input_parameters):
        """Save prediction to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions 
                (user_id, disease_type, prediction_result, risk_probability, 
                 risk_level, input_parameters)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, disease_type, prediction_result, risk_probability, 
                  risk_level, str(input_parameters)))
            
            prediction_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, "Prediction saved!", prediction_id
            
        except Exception as e:
            return False, f"Error saving prediction: {str(e)}", None
    
    def get_user_predictions(self, user_id, disease_type=None):
        """Get all predictions for a user, optionally filtered by disease type"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if disease_type:
                cursor.execute('''
                    SELECT * FROM predictions 
                    WHERE user_id = ? AND disease_type = ?
                    ORDER BY prediction_date DESC
                ''', (user_id, disease_type))
            else:
                cursor.execute('''
                    SELECT * FROM predictions 
                    WHERE user_id = ?
                    ORDER BY prediction_date DESC
                ''', (user_id,))
            
            predictions = cursor.fetchall()
            conn.close()
            
            return [dict(pred) for pred in predictions]
            
        except Exception as e:
            print(f"Error getting predictions: {e}")
            return []
    
    def get_prediction_count(self, user_id):
        """Get total number of predictions for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) as count FROM predictions WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
            
        except Exception as e:
            print(f"Error getting prediction count: {e}")
            return 0
    
    def get_prediction_stats(self, user_id):
        """Get statistics about user's predictions"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Count by disease type
            cursor.execute('''
                SELECT disease_type, COUNT(*) as count
                FROM predictions
                WHERE user_id = ?
                GROUP BY disease_type
            ''', (user_id,))
            
            disease_counts = {row['disease_type']: row['count'] 
                            for row in cursor.fetchall()}
            
            # Count by risk level
            cursor.execute('''
                SELECT risk_level, COUNT(*) as count
                FROM predictions
                WHERE user_id = ?
                GROUP BY risk_level
            ''', (user_id,))
            
            risk_counts = {row['risk_level']: row['count'] 
                          for row in cursor.fetchall()}
            
            conn.close()
            
            return {
                'by_disease': disease_counts,
                'by_risk': risk_counts
            }
            
        except Exception as e:
            print(f"Error getting prediction stats: {e}")
            return {'by_disease': {}, 'by_risk': {}}
    
    def update_user_profile(self, user_id, full_name=None, age=None, gender=None):
        """Update user profile information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if full_name is not None:
                updates.append("full_name = ?")
                params.append(full_name)
            if age is not None:
                updates.append("age = ?")
                params.append(age)
            if gender is not None:
                updates.append("gender = ?")
                params.append(gender)
            
            if updates:
                params.append(user_id)
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
            
            conn.close()
            return True, "Profile updated successfully!"
            
        except Exception as e:
            return False, f"Error updating profile: {str(e)}"
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, "User not found"
            
            if not bcrypt.checkpw(old_password.encode('utf-8' ), result[0]):
                conn.close()
                return False, "Current password is incorrect"
            
            # Hash new password
            new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
            # Update password
            cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user_id))
            conn.commit()
            conn.close()
            
            return True, "Password changed successfully"
        except Exception as e:
            return False, f"Error changing password: {str(e)}"
    
    def delete_account(self, user_id):
        """Delete user account and all associated data"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Delete predictions
            cursor.execute('DELETE FROM predictions WHERE user_id = ?', (user_id,))
            
            # Delete user
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            return True, "Account deleted successfully"
        except Exception as e:
            return False, f"Error deleting account: {str(e)}"
