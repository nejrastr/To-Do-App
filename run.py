from app import create_app, db
import json
from app.models import User



app = create_app()

if __name__ == '__main__':
    with app.app_context():
      
        #db.drop_all()
        db.create_all()
        user = User.query.first()  
        progress = user.calculate_task_progress()

        print(f'Procent of completed tasks: {progress}%')
        goal_progress = user.calculate_goal_progress()
        print(f"Daily Goal Progress: {goal_progress[0]}%")
        print(f"Weekly Goal Progress: {goal_progress[1]}%")
        print(f"Monthly Goal Progress: {goal_progress[2]}%")
        print(f"Yearly Goal Progress: {goal_progress[3]}%")

        
        print(goal_progress)
        
       
    app.run(debug=True)
