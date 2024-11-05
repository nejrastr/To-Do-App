from app import create_app, db
import json



app = create_app()

if __name__ == '__main__':
    with app.app_context():
      
        #db.drop_all()
        db.create_all()

       
    app.run(debug=True)
