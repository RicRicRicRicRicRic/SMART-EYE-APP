from app.config.settings import settings

if __name__ == "__main__":
    print("Database connection string (without password):")
    print(f"mysql+pymysql://{settings.db_user}:***@{settings.db_host}:{settings.db_port}/{settings.db_name}")