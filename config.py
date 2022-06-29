from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "hansung_grade_backend"
    LOGIN_URL: str
    GRADE_URL: str
    INFO_URL: str
    NOW_SEMESTER_GRADE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
