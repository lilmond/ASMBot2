import sqlite3
import os

database = sqlite3.connect(f"{os.path.dirname(__file__)}/database.db", check_same_thread=False)


def _initialize():
    database.execute('''CREATE TABLE IF NOT EXISTS "USERS" (
        DISCORD_ID      INTEGER     NOT NULL,
        TWITTER_ID      INTEGER,
        XRP_ADDRESS     TEXT,
        SOCIAL_CREDITS  INTEGER     NOT NULL,
        SOCIAL_TOKENS   INTEGER     NOT NULL,
        SPENT_XRP       INTEGER     NOT NULL,
        LAST_DAILY      INTEGER
    );''')

    database.execute('''CREATE TABLE IF NOT EXISTS "XAMAN_WALLETS" (
        DISCORD_ID      INTEGER     NOT NULL,
        XRP_ADDRESS     TEXT,
        UUID            TEXT        NOT NULL
    );''')

    database.commit()

_initialize()


class User(object):
    def __init__(self, discord_id: int, twitter_id: int, xrp_address: str, social_credits: int, social_tokens: int, spent_xrp: int, last_daily: int):
        self.discord_id = discord_id
        self.twitter_id = twitter_id
        self.xrp_address = xrp_address
        self.social_credits = social_credits
        self.social_tokens = social_tokens
        self.spent_xrp = spent_xrp
        self.last_daily = last_daily
    

    def user_points(self, action: str, currency: str, value: int):
        if not action in ["add", "deduct", "set"]:
            return
        
        if not currency in ["social_credits", "social_tokens"]:
            return

        match action:
            case "add":
                database.execute(f'UPDATE USERS SET {currency.upper()}={currency.upper()}+{value} WHERE DISCORD_ID={self.discord_id};')
            case "deduct":
                database.execute(f'UPDATE USERS SET {currency.upper()}={currency.upper()}-{value} WHERE DISCORD_ID={self.discord_id};')
            case "set":
                database.execute(f'UPDATE USERS SET {currency.upper()}={value} WHERE DISCORD_ID={self.discord_id};')

        database.commit()
    

    def set_xrp_address(self, xrp_address: str):
        database.execute(f'UPDATE USERS SET XRP_ADDRESS="{xrp_address}" WHERE DISCORD_ID={self.discord_id};')
        database.commit()

    
    def set_last_daily(self, epoch: float):
        database.execute(f'UPDATE USERS SET LAST_DAILY={epoch} WHERE DISCORD_ID={self.discord_id};')
        database.commit()


class Users(object):
    def __init__(self):
        self.new_social_credits = 100
        self.new_social_tokens = 0


    def add_user(self, discord_id: int) -> None:
        database.execute(f'INSERT INTO USERS (DISCORD_ID, SOCIAL_CREDITS, SOCIAL_TOKENS, SPENT_XRP) VALUES ({discord_id}, {self.new_social_credits}, {self.new_social_tokens}, 0);')
        database.commit()


    def get_user(self, discord_id: int) -> User:
        fetched = database.execute(f'SELECT * FROM USERS WHERE DISCORD_ID={discord_id};').fetchone()

        if not fetched:
            self.add_user(discord_id=discord_id)
            return self.get_user(discord_id=discord_id)

        return User(*fetched)
    
    def get_leaderboard(self, stats: str):
        if not stats in ["social_credits", "social_tokens", "spent_xrp"]:
            return

        return [self.get_user(user[0]) for user in database.execute(f'SELECT * FROM USERS WHERE {stats.upper()}>0 ORDER BY {stats.upper()} DESC LIMIT 10;').fetchall()]


class UuidNotFound(Exception):
    pass


class XamanWallets(object):
    def __init__(self):
        pass


    def get_discord_id(self, discord_id: int):
        return database.execute(f'SELECT * FROM XAMAN_WALLETS WHERE DISCORD_ID={discord_id};').fetchone()


    def get_uuid(self, uuid: str):
        return database.execute(f'SELECT * FROM XAMAN_WALLETS WHERE UUID="{uuid}";').fetchone()


    def register_uuid(self, discord_id: int, uuid: str):
        # Check if the user already exists in the registration table.
        user = self.get_discord_id(discord_id=discord_id)

        # Edit user's uuid if they already exist. Append if not.
        if user:
            database.execute(f'UPDATE XAMAN_WALLETS SET UUID="{uuid}" WHERE DISCORD_ID={discord_id};')
        else:
            database.execute(f'INSERT INTO XAMAN_WALLETS (DISCORD_ID, UUID) VALUES ({discord_id}, "{uuid}");')
        
        database.commit()
    

    def verify_uuid(self, uuid: str, xrp_address: str):
        uuid_info = self.get_uuid(uuid=uuid)

        if not uuid_info:
            raise UuidNotFound(f"UuidNotFound: {uuid} xrp_address: {xrp_address}")
        
        discord_id = uuid_info[0]
        
        database.execute(f'DELETE FROM XAMAN_WALLETS WHERE DISCORD_ID={discord_id};')

        # This will automatically add the user to the USERS table if their user ID does not exist.
        users_db = Users()
        user = users_db.get_user(discord_id=discord_id)
        user.set_xrp_address(xrp_address=xrp_address)

