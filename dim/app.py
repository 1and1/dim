from dim import create_app
import os.path

testing = os.getenv("DIM_TESTING", False)
db_mode = os.getenv("DIM_DB_MODE", None)

application = create_app(db_mode, testing)
