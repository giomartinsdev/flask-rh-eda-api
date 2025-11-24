from flask_restx import Api

api = Api(
    title="RH EDA API",
    version="1.0",
    description="API para gerenciamento de recursos humanos utilizando EDA",
    doc="/docs",
)
