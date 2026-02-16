"""
Endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from typing import Dict, Any, Optional, List

from ..database import activities_collection, teachers_collection

router = APIRouter(
    prefix="/activities",
    tags=["activities"]
)

@router.get("", response_model=Dict[str, Any])
@router.get("/", response_model=Dict[str, Any])
def get_activities(
    day: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all activities with their details, with optional filtering by day and time
    
    - day: Filter activities occurring on this day (e.g., 'Monday', 'Tuesday')
    - start_time: Filter activities starting at or after this time (24-hour format, e.g., '14:30')
    - end_time: Filter activities ending at or before this time (24-hour format, e.g., '17:00')
    """
    # Build the query based on provided filters
    query = {}
    
    if day:
        query["schedule_details.days"] = {"$in": [day]}
    
    if start_time:
        query["schedule_details.start_time"] = {"$gte": start_time}
    
    if end_time:
        query["schedule_details.end_time"] = {"$lte": end_time}
    
    # Query the database
    activities = {}
    for activity in activities_collection.find(query):
        name = activity.pop('_id')
        activities[name] = activity
    
    return activities

@router.get("/days", response_model=List[str])
def get_available_days() -> List[str]:
    """Get a list of all days that have activities scheduled"""
    # Aggregate to get unique days across all activities
    pipeline = [
        {"$unwind": "$schedule_details.days"},
        {"$group": {"_id": "$schedule_details.days"}},
        {"$sort": {"_id": 1}}  # Sort days alphabetically
    ]
    
    days = []
    for day_doc in activities_collection.aggregate(pipeline):
        days.append(day_doc["_id"])
    
    return days

@router.post("/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, teacher_username: Optional[str] = Query(None)):
    """Sign up a student for an activity - requires teacher authentication"""
    # Check teacher authentication
    if not teacher_username:
        raise HTTPException(status_code=401, detail="Authentication required for this action")
    
    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(status_code=401, detail="Invalid teacher credentials")
    
    # Get the activity
    activity = activities_collection.find_one({"_id": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400, detail="Already signed up for this activity")

    # Add student to participants
    result = activities_collection.update_one(
        {"_id": activity_name},
        {"$push": {"participants": email}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update activity")
    
    return {"message": f"Signed up {email} for {activity_name}"}

@router.post("/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, teacher_username: Optional[str] = Query(None)):
    """Remove a student from an activity - requires teacher authentication"""
    # Check teacher authentication
    if not teacher_username:
        raise HTTPException(status_code=401, detail="Authentication required for this action")
    
    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(status_code=401, detail="Invalid teacher credentials")
    
    # Get the activity
    activity = activities_collection.find_one({"_id": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400, detail="Not registered for this activity")

    # Remove student from participants
    result = activities_collection.update_one(
        {"_id": activity_name},
        {"$pull": {"participants": email}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update activity")
    
    return {"message": f"Unregistered {email} from {activity_name}"}

@router.get("/statistics")
def get_activity_statistics() -> Dict[str, Any]:
    """
    Get statistics about all activities including:
    - Total number of activities
    - Total students enrolled
    - Most popular activity
    - Activities by day of week
    """
    # Get all activities from database
    all_activities = list(activities_collection.find({}))
    
    if not all_activities:
        return {
            "total_activities": 0,
            "total_students_enrolled": 0,
            "most_popular_activity": None,
            "activities_by_day": {},
            "average_participants_per_activity": 0
        }
    
    # Calculate statistics
    total_activities = len(all_activities)
    total_students = sum(len(activity.get("participants", [])) for activity in all_activities)
    
    # Find most popular activity
    most_popular = max(all_activities, key=lambda x: len(x.get("participants", [])))
    most_popular_name = most_popular.get("_id")
    most_popular_count = len(most_popular.get("participants", []))
    
    # Count activities by day of week
    activities_by_day = {}
    for activity in all_activities:
        schedule_details = activity.get("schedule_details", {})
        days = schedule_details.get("days", [])
        for day in days:
            activities_by_day[day] = activities_by_day.get(day, 0) + 1
    
    # Calculate average
    average_participants = round(total_students / total_activities, 2) if total_activities > 0 else 0
    
    return {
        "total_activities": total_activities,
        "total_students_enrolled": total_students,
        "most_popular_activity": {
            "name": most_popular_name,
            "participant_count": most_popular_count
        },
        "activities_by_day": activities_by_day,
        "average_participants_per_activity": average_participants
    }