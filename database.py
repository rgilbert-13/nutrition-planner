# database.py
import sqlite3
from datetime import date
import streamlit as st

DB_PATH = "platemate.db"

def init_db():
    """Create tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Meals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            meal_type TEXT,
            meal_date DATE NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_meal(description, calories, protein, carbs, fat, meal_type=None, image_url=None):
    """Save a meal to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO meals (description, calories, protein, carbs, fat, meal_type, meal_date, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (description, calories, protein, carbs, fat, meal_type, date.today(), image_url))
    
    conn.commit()
    conn.close()

def get_todays_meals():
    """Get all meals for today"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, description, calories, protein, carbs, fat, meal_type, meal_date
        FROM meals
        WHERE meal_date = ?
        ORDER BY created_at DESC
    ''', (date.today(),))
    
    meals = cursor.fetchall()
    conn.close()
    
    return meals

def get_todays_totals():
    """Get total nutrition for today"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            SUM(calories) as total_calories,
            SUM(protein) as total_protein,
            SUM(carbs) as total_carbs,
            SUM(fat) as total_fat,
            COUNT(*) as meal_count
        FROM meals
        WHERE meal_date = ?
    ''', (date.today(),))
    
    totals = cursor.fetchone()
    conn.close()
    
    return {
        'calories': totals[0] or 0,
        'protein': totals[1] or 0,
        'carbs': totals[2] or 0,
        'fat': totals[3] or 0,
        'count': totals[4] or 0
    }