export DATABASE_TEST_URL=sqlite:////tmp/sqlite_test.db
export DATABASE_URL=sqlite:////tmp/sqlite_dev.db
export FLASK_APP=project/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=project.config.DevelopmentConfig
python manage.py run -h 0.0.0.0 -p 5000
