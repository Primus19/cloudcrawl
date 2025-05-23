from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    from src.api.aws_accounts import aws_accounts_bp
    app.register_blueprint(aws_accounts_bp)
    
    from src.api.aws_resources import aws_resources_bp
    app.register_blueprint(aws_resources_bp)
    
    from src.api.terraform import terraform_bp
    app.register_blueprint(terraform_bp)
    
    # Add direct health endpoint
    @app.route("/api/v1/health")
    def health():
        return {"status": "ok"}
    
    return app
