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

        goal_progress_daily, goal_progress_weekly, goal_progress_monthly, goal_progress_yearly = user.calculate_goal_progress()
        print(f"Daily Goal Progress: {goal_progress_daily}%")
        print(f"Weekly Goal Progress: {goal_progress_weekly}%")
        print(f"Monthly Goal Progress: {goal_progress_monthly}%")
        print(f"Yearly Goal Progress: {goal_progress_yearly}%")
        

        
        
        
       
    app.run(debug=True)
