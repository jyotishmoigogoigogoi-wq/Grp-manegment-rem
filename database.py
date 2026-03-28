"""
˹ʀᴇᴍ˼ Bot Database Module
Neon PostgreSQL connection and all queries
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
import logging

from config import DATABASE_URL, DB_TABLES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """Database manager for Neon PostgreSQL"""
    
    def __init__(self):
        self.connection_string = DATABASE_URL
        self._init_tables()
    
    @contextmanager
    def _get_cursor(self, commit: bool = False):
        """Context manager for database cursor"""
        conn = None
        try:
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def _init_tables(self):
        """Initialize all database tables"""
        try:
            with self._get_cursor(commit=True) as cur:
                for table_name, create_query in DB_TABLES.items():
                    cur.execute(create_query)
                    logger.info(f"Table '{table_name}' initialized")
            logger.info("All database tables initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing tables: {e}")
    
    # ============== USER METHODS ==============
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, 
                 last_name: str = None) -> bool:
        """Add or update user"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO users (user_id, username, first_name, last_name, last_active)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (user_id) 
                    DO UPDATE SET 
                        username = EXCLUDED.username,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        last_active = CURRENT_TIMESTAMP
                """, (user_id, username, first_name, last_name))
            return True
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                return dict(cur.fetchone()) if cur.fetchone() else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def increment_user_commands(self, user_id: int) -> bool:
        """Increment user's command count"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    UPDATE users 
                    SET command_count = command_count + 1, last_active = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                """, (user_id,))
            return True
        except Exception as e:
            logger.error(f"Error incrementing commands: {e}")
            return False
    
    def get_total_users(self) -> int:
        """Get total user count"""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT COUNT(*) as count FROM users")
                result = cur.fetchone()
                return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0
    
    # ============== GROUP METHODS ==============
    
    def add_group(self, group_id: int, group_name: str, owner_id: int) -> bool:
        """Add or update group"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO groups (group_id, group_name, owner_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (group_id) 
                    DO UPDATE SET 
                        group_name = EXCLUDED.group_name
                """, (group_id, group_name, owner_id))
            return True
        except Exception as e:
            logger.error(f"Error adding group: {e}")
            return False
    
    def get_group(self, group_id: int) -> Optional[Dict]:
        """Get group by ID"""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT * FROM groups WHERE group_id = %s", (group_id,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Error getting group: {e}")
            return None
    
    def update_group_setting(self, group_id: int, setting: str, value: Any) -> bool:
        """Update a group setting"""
        try:
            with self._get_cursor(commit=True) as cur:
                # Handle boolean values
                if isinstance(value, bool):
                    cur.execute(f"""
                        UPDATE groups 
                        SET {setting} = %s
                        WHERE group_id = %s
                    """, (value, group_id))
                else:
                    cur.execute(f"""
                        UPDATE groups 
                        SET {setting} = %s
                        WHERE group_id = %s
                    """, (value, group_id))
            return True
        except Exception as e:
            logger.error(f"Error updating group setting: {e}")
            return False
    
    def get_total_groups(self) -> int:
        """Get total group count"""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT COUNT(*) as count FROM groups")
                result = cur.fetchone()
                return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting group count: {e}")
            return 0
    
    # ============== GROUP MEMBERS METHODS ==============
    
    def add_group_member(self, group_id: int, user_id: int) -> bool:
        """Add member to group"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO group_members (group_id, user_id)
                    VALUES (%s, %s)
                    ON CONFLICT (group_id, user_id) DO NOTHING
                """, (group_id, user_id))
            return True
        except Exception as e:
            logger.error(f"Error adding group member: {e}")
            return False
    
    def remove_group_member(self, group_id: int, user_id: int) -> bool:
        """Remove member from group"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    DELETE FROM group_members 
                    WHERE group_id = %s AND user_id = %s
                """, (group_id, user_id))
            return True
        except Exception as e:
            logger.error(f"Error removing group member: {e}")
            return False
    
    def get_group_member(self, group_id: int, user_id: int) -> Optional[Dict]:
        """Get group member info"""
        try:
            with self._get_cursor() as cur:
                cur.execute("""
                    SELECT * FROM group_members 
                    WHERE group_id = %s AND user_id = %s
                """, (group_id, user_id))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Error getting group member: {e}")
            return None
    
    def increment_warn(self, group_id: int, user_id: int) -> int:
        """Increment warning count and return new count"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO group_members (group_id, user_id, warn_count)
                    VALUES (%s, %s, 1)
                    ON CONFLICT (group_id, user_id) 
                    DO UPDATE SET warn_count = group_members.warn_count + 1
                    RETURNING warn_count
                """, (group_id, user_id))
                result = cur.fetchone()
                return result['warn_count'] if result else 0
        except Exception as e:
            logger.error(f"Error incrementing warn: {e}")
            return 0
    
    def reset_warns(self, group_id: int, user_id: int) -> bool:
        """Reset warnings for a user"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    UPDATE group_members 
                    SET warn_count = 0
                    WHERE group_id = %s AND user_id = %s
                """, (group_id, user_id))
            return True
        except Exception as e:
            logger.error(f"Error resetting warns: {e}")
            return False
    
    def set_mute(self, group_id: int, user_id: int, muted: bool, until: datetime = None) -> bool:
        """Set mute status for a user"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO group_members (group_id, user_id, is_muted, mute_until)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (group_id, user_id) 
                    DO UPDATE SET is_muted = EXCLUDED.is_muted, mute_until = EXCLUDED.mute_until
                """, (group_id, user_id, muted, until))
            return True
        except Exception as e:
            logger.error(f"Error setting mute: {e}")
            return False
    
    # ============== USER SESSIONS METHODS ==============
    
    def set_user_session(self, user_id: int, chat_id: int, message_id: int, 
                         menu: str, data: Dict = None) -> bool:
        """Set or update user session for replaceable messages"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO user_sessions (user_id, chat_id, message_id, current_menu, session_data)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id, chat_id) 
                    DO UPDATE SET 
                        message_id = EXCLUDED.message_id,
                        current_menu = EXCLUDED.current_menu,
                        session_data = EXCLUDED.session_data,
                        updated_at = CURRENT_TIMESTAMP
                """, (user_id, chat_id, message_id, menu, json.dumps(data or {})))
            return True
        except Exception as e:
            logger.error(f"Error setting session: {e}")
            return False
    
    def get_user_session(self, user_id: int, chat_id: int) -> Optional[Dict]:
        """Get user session"""
        try:
            with self._get_cursor() as cur:
                cur.execute("""
                    SELECT * FROM user_sessions 
                    WHERE user_id = %s AND chat_id = %s
                """, (user_id, chat_id))
                result = cur.fetchone()
                if result:
                    data = dict(result)
                    data['session_data'] = json.loads(data.get('session_data', '{}'))
                    return data
                return None
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            return None
    
    def update_user_session_menu(self, user_id: int, chat_id: int, menu: str) -> bool:
        """Update just the menu in user session"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    UPDATE user_sessions 
                    SET current_menu = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND chat_id = %s
                """, (menu, user_id, chat_id))
            return True
        except Exception as e:
            logger.error(f"Error updating session menu: {e}")
            return False
    
    # ============== BOT CONFIG METHODS ==============
    
    def set_config(self, key: str, value: str) -> bool:
        """Set bot configuration value"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO bot_config (config_key, config_value)
                    VALUES (%s, %s)
                    ON CONFLICT (config_key) 
                    DO UPDATE SET 
                        config_value = EXCLUDED.config_value,
                        updated_at = CURRENT_TIMESTAMP
                """, (key, value))
            return True
        except Exception as e:
            logger.error(f"Error setting config: {e}")
            return False
    
    def get_config(self, key: str, default: str = None) -> str:
        """Get bot configuration value"""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT config_value FROM bot_config WHERE config_key = %s", (key,))
                result = cur.fetchone()
                return result['config_value'] if result else default
        except Exception as e:
            logger.error(f"Error getting config: {e}")
            return default
    
    # ============== CAPTCHA METHODS ==============
    
    def create_captcha(self, user_id: int, chat_id: int, captcha_type: str, 
                       answer: str) -> int:
        """Create new captcha session"""
        try:
            expires = datetime.now() + timedelta(minutes=5)
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO captcha_sessions (user_id, chat_id, captcha_type, captcha_answer, expires_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING session_id
                """, (user_id, chat_id, captcha_type, answer, expires))
                result = cur.fetchone()
                return result['session_id'] if result else 0
        except Exception as e:
            logger.error(f"Error creating captcha: {e}")
            return 0
    
    def get_captcha(self, user_id: int, chat_id: int) -> Optional[Dict]:
        """Get active captcha for user"""
        try:
            with self._get_cursor() as cur:
                cur.execute("""
                    SELECT * FROM captcha_sessions 
                    WHERE user_id = %s AND chat_id = %s AND verified = FALSE AND expires_at > CURRENT_TIMESTAMP
                    ORDER BY created_at DESC LIMIT 1
                """, (user_id, chat_id))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Error getting captcha: {e}")
            return None
    
    def verify_captcha(self, session_id: int) -> bool:
        """Mark captcha as verified"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    UPDATE captcha_sessions 
                    SET verified = TRUE
                    WHERE session_id = %s
                """, (session_id,))
            return True
        except Exception as e:
            logger.error(f"Error verifying captcha: {e}")
            return False
    
    def delete_captcha(self, session_id: int) -> bool:
        """Delete captcha session"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("DELETE FROM captcha_sessions WHERE session_id = %s", (session_id,))
            return True
        except Exception as e:
            logger.error(f"Error deleting captcha: {e}")
            return False
    
    # ============== FILTER METHODS ==============
    
    def add_filter(self, group_id: int, keyword: str, response: str, created_by: int) -> bool:
        """Add word filter to group"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO filters (group_id, keyword, response, created_by)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (group_id, keyword.lower(), response, created_by))
            return True
        except Exception as e:
            logger.error(f"Error adding filter: {e}")
            return False
    
    def remove_filter(self, group_id: int, keyword: str) -> bool:
        """Remove word filter from group"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    DELETE FROM filters 
                    WHERE group_id = %s AND keyword = %s
                """, (group_id, keyword.lower()))
            return True
        except Exception as e:
            logger.error(f"Error removing filter: {e}")
            return False
    
    def get_filters(self, group_id: int) -> List[Dict]:
        """Get all filters for a group"""
        try:
            with self._get_cursor() as cur:
                cur.execute("""
                    SELECT * FROM filters WHERE group_id = %s
                """, (group_id,))
                return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error getting filters: {e}")
            return []
    
    def get_filter_response(self, group_id: int, keyword: str) -> Optional[str]:
        """Get filter response for keyword"""
        try:
            with self._get_cursor() as cur:
                cur.execute("""
                    SELECT response FROM filters 
                    WHERE group_id = %s AND keyword = %s
                """, (group_id, keyword.lower()))
                result = cur.fetchone()
                return result['response'] if result else None
        except Exception as e:
            logger.error(f"Error getting filter response: {e}")
            return None
    
    # ============== LOG METHODS ==============
    
    def add_log(self, group_id: int, admin_id: int, action: str, 
                target_id: int = None, reason: str = None) -> bool:
        """Add admin action log"""
        try:
            with self._get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO logs (group_id, admin_id, action, target_id, reason)
                    VALUES (%s, %s, %s, %s, %s)
                """, (group_id, admin_id, action, target_id, reason))
            return True
        except Exception as e:
            logger.error(f"Error adding log: {e}")
            return False
    
    def get_logs(self, group_id: int, limit: int = 50) -> List[Dict]:
        """Get admin action logs for a group"""
        try:
            with self._get_cursor() as cur:
                cur.execute("""
                    SELECT * FROM logs 
                    WHERE group_id = %s 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (group_id, limit))
                return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return []
    
    # ============== STATS METHODS ==============
    
    def get_stats(self) -> Dict:
        """Get bot statistics"""
        try:
            with self._get_cursor() as cur:
                stats = {}
                
                cur.execute("SELECT COUNT(*) as count FROM users")
                stats['total_users'] = cur.fetchone()['count']
                
                cur.execute("SELECT COUNT(*) as count FROM groups")
                stats['total_groups'] = cur.fetchone()['count']
                
                cur.execute("SELECT SUM(command_count) as total FROM users")
                result = cur.fetchone()
                stats['total_commands'] = result['total'] if result['total'] else 0
                
                cur.execute("SELECT COUNT(*) as count FROM group_members")
                stats['total_members'] = cur.fetchone()['count']
                
                cur.execute("SELECT COUNT(*) as count FROM captcha_sessions")
                stats['total_captchas'] = cur.fetchone()['count']
                
                return stats
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                'total_users': 0,
                'total_groups': 0,
                'total_commands': 0,
                'total_members': 0,
                'total_captchas': 0
            }
    
    def get_all_groups(self) -> List[int]:
        """Get all group IDs for broadcast"""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT group_id FROM groups")
                return [row['group_id'] for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error getting groups: {e}")
            return []
    
    def get_all_users(self) -> List[int]:
        """Get all user IDs for broadcast"""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT user_id FROM users")
                return [row['user_id'] for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []


# Create global database instance
db = Database()
