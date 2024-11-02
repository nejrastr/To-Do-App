from app import create_app, db
import json

def load_static_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

app = create_app()

if __name__ == '__main__':
    with app.app_context():
      
       # db.drop_all()
        db.create_all()

       

       
    app.run(debug=True)
