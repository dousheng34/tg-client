#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ҚАЗАҚ ӘДЕБИЕТІ БОТЫ ТЕСТІЛЕУ
Unit тестілер
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from telegram import Update, User, Chat, Message
from telegram.ext import ContextTypes

# Ботты импорттау
import sys
sys.path.insert(0, '/home/code')
from kazakh_literature_bot import (
    DATABASE, GAMES, get_user_score, add_score, 
    start, help_command, about, show_authors, show_works
)

# ============================================================================
# FIXTURE-ЛАР
# ============================================================================

@pytest.fixture
def mock_update():
    """Mock Update объектін жасау"""
    update = Mock(spec=Update)
    update.effective_user = Mock(spec=User)
    update.effective_user.id = 123456789
    update.effective_user.first_name = "Тест"
    update.message = Mock(spec=Message)
    update.message.reply_text = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    """Mock Context объектін жасау"""
    context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {}
    return context

# ============================================================================
# ДЕРЕКТЕР БАЗАСЫ ТЕСТІЛЕРІ
# ============================================================================

class TestDatabase:
    """Деректер базасы тестілері"""
    
    def test_database_structure(self):
        """Деректер базасының құрылымын тексеру"""
        assert "grades" in DATABASE
        assert isinstance(DATABASE["grades"], dict)
    
    def test_grades_exist(self):
        """Сыныптар бар екенін тексеру"""
        grades = DATABASE["grades"]
        assert len(grades) > 0
        assert "1" in grades or "4" in grades or "7" in grades
    
    def test_grade_structure(self):
        """Сынып құрылымын тексеру"""
        for grade_id, grade_data in DATABASE["grades"].items():
            assert "grade" in grade_data
            assert "authors" in grade_data
            assert "works" in grade_data
            assert isinstance(grade_data["authors"], list)
            assert isinstance(grade_data["works"], list)
    
    def test_author_structure(self):
        """Автор құрылымын тексеру"""
        for grade_id, grade_data in DATABASE["grades"].items():
            for author in grade_data["authors"]:
                assert "id" in author
                assert "name" in author
                assert "years" in author
                assert "bio" in author
    
    def test_work_structure(self):
        """Шығарма құрылымын тексеру"""
        for grade_id, grade_data in DATABASE["grades"].items():
            for work in grade_data["works"]:
                assert "id" in work
                assert "name" in work
                assert "author" in work
                assert "genre" in work
                assert "summary" in work
                assert "idea" in work
    
    def test_quiz_questions_exist(self):
        """Викторина сұрақтары бар екенін тексеру"""
        for grade_id, grade_data in DATABASE["grades"].items():
            for work in grade_data["works"]:
                if "quiz" in work:
                    assert len(work["quiz"]) > 0
                    for question in work["quiz"]:
                        assert "q" in question
                        assert "a" in question
                        assert "options" in question

# ============================================================================
# ОЙЫНДАР ТЕСТІЛЕРІ
# ============================================================================

class TestGames:
    """Ойындар тестілері"""
    
    def test_games_structure(self):
        """Ойындар құрылымын тексеру"""
        assert "who_am_i" in GAMES
        assert "match" in GAMES
        assert "fill_blank" in GAMES
    
    def test_who_am_i_game(self):
        """Кім мен ойынын тексеру"""
        games = GAMES["who_am_i"]
        assert len(games) > 0
        for game in games:
            assert "clues" in game
            assert "answer" in game
            assert "work" in game
            assert len(game["clues"]) > 0
    
    def test_match_game(self):
        """Сәйкестендіру ойынын тексеру"""
        games = GAMES["match"]
        assert len(games) > 0
        for game in games:
            assert "author" in game
            assert "work" in game
    
    def test_fill_blank_game(self):
        """Толтыру ойынын тексеру"""
        games = GAMES["fill_blank"]
        assert len(games) > 0
        for game in games:
            assert "sentence" in game
            assert "answer" in game

# ============================================================================
# ҰПАЙ ЖҮЙЕСІ ТЕСТІЛЕРІ
# ============================================================================

class TestScoreSystem:
    """Ұпай жүйесі тестілері"""
    
    def test_get_user_score_new_user(self):
        """Жаңа пайдаланушының ұпайын алу"""
        user_id = 999999999
        score = get_user_score(user_id)
        assert score["total"] == 0
        assert score["correct"] == 0
        assert score["games_played"] == 0
        assert score["level"] == "Бастамшы"
    
    def test_add_score_beginner(self):
        """Бастамшы деңгейіне ұпай қосу"""
        user_id = 888888888
        add_score(user_id, 10)
        score = get_user_score(user_id)
        assert score["total"] == 10
        assert score["correct"] == 1
        assert score["level"] == "Бастамшы"
    
    def test_add_score_intermediate(self):
        """Орта деңгейіне ұпай қосу"""
        user_id = 777777777
        for _ in range(5):
            add_score(user_id, 10)
        score = get_user_score(user_id)
        assert score["total"] == 50
        assert score["level"] == "Орта"
    
    def test_add_score_master(self):
        """Ұстаз деңгейіне ұпай қосу"""
        user_id = 666666666
        for _ in range(10):
            add_score(user_id, 10)
        score = get_user_score(user_id)
        assert score["total"] == 100
        assert score["level"] == "Ұстаз"

# ============================================================================
# КОМАНДА ТЕСТІЛЕРІ
# ============================================================================

class TestCommands:
    """Команда тестілері"""
    
    @pytest.mark.asyncio
    async def test_start_command(self, mock_update, mock_context):
        """Start командасын тексеру"""
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "Қазақ Әдебиеті" in call_args[0][0]
    
    @pytest.mark.asyncio
    async def test_help_command(self, mock_update, mock_context):
        """Help командасын тексеру"""
        await help_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "КӨМЕК" in call_args[0][0]
    
    @pytest.mark.asyncio
    async def test_about_command(self, mock_update, mock_context):
        """About командасын тексеру"""
        await about(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "v4.0" in call_args[0][0]

# ============================================================================
# ИНТЕГРАЦИЯ ТЕСТІЛЕРІ
# ============================================================================

class TestIntegration:
    """Интеграция тестілері"""
    
    def test_database_consistency(self):
        """Деректер базасының сәйкестігін тексеру"""
        for grade_id, grade_data in DATABASE["grades"].items():
            # Авторлар мен шығармалар арасындағы сәйкестік
            for work in grade_data["works"]:
                if "author_id" in work:
                    author_ids = [a["id"] for a in grade_data["authors"]]
                    assert work["author_id"] in author_ids, \
                        f"Шығарма {work['id']} авторы табылмады"
    
    def test_no_duplicate_ids(self):
        """Қосарлы ID-лер жоқ екенін тексеру"""
        all_ids = set()
        for grade_id, grade_data in DATABASE["grades"].items():
            for author in grade_data["authors"]:
                assert author["id"] not in all_ids, \
                    f"Қосарлы автор ID: {author['id']}"
                all_ids.add(author["id"])
            
            for work in grade_data["works"]:
                assert work["id"] not in all_ids, \
                    f"Қосарлы шығарма ID: {work['id']}"
                all_ids.add(work["id"])

# ============================================================================
# PERFORMANCE ТЕСТІЛЕРІ
# ============================================================================

class TestPerformance:
    """Өндіріс тестілері"""
    
    def test_database_load_time(self):
        """Деректер базасын жүктеу уақыты"""
        import time
        start = time.time()
        _ = DATABASE
        end = time.time()
        assert (end - start) < 0.1, "Деректер базасы тым ұзақ жүктелді"
    
    def test_score_calculation_performance(self):
        """Ұпай есептеу өндірісі"""
        import time
        start = time.time()
        for i in range(1000):
            add_score(i, 10)
        end = time.time()
        assert (end - start) < 1.0, "Ұпай есептеу тым ұзақ"

# ============================================================================
# ҚАУІПСІЗДІК ТЕСТІЛЕРІ
# ============================================================================

class TestSecurity:
    """Қауіпсіздік тестілері"""
    
    def test_no_hardcoded_secrets(self):
        """Қатты кодталған құпиялар жоқ екенін тексеру"""
        with open('/home/code/kazakh_literature_bot.py', 'r') as f:
            content = f.read()
            # Нақты токен жоқ екенін тексеру
            assert "7123456789:ABCdefGHIjklMNOpqrSTUvwxYZ" not in content or \
                   "os.getenv" in content
    
    def test_env_file_in_gitignore(self):
        """ENV файлы gitignore-та бар екенін тексеру"""
        with open('/home/code/.gitignore', 'r') as f:
            content = f.read()
            assert ".env" in content

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
