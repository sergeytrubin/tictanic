# Launch dev server
from app import create_app

application = create_app()
application.run(host='0.0.0.0', port=8000, debug=True)
