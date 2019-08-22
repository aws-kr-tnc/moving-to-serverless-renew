export DATABASE_TEST_URL=sqlite:////tmp/sqlite_test.database
export DATABASE_URL=sqlite:////tmp/sqlite_dev.database
export FLASK_APP=cloudalbum/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=cloudalbum.config.DevelopmentConfig
python manage.py run -h 0.0.0.0 -p 5000
