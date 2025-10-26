def register_blueprints(app):
    """Register application blueprint"""
    
    # Main blueprint
    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    