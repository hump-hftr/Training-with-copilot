"""
In-memory database for Mergington High School API
Using simple dictionaries for easy development and testing
"""

from argon2 import PasswordHasher
from typing import Dict, Any, Optional, List
import copy

# In-memory storage
activities_data: Dict[str, Any] = {}
teachers_data: Dict[str, Any] = {}

# Mock collection class to mimic MongoDB collection interface
class InMemoryCollection:
    def __init__(self, data_dict: Dict):
        self.data = data_dict
    
    def find(self, query: Optional[Dict] = None):
        """Find documents matching query"""
        if query is None or not query:
            results = []
            for doc_id, doc in self.data.items():
                doc_copy = copy.deepcopy(doc)
                if "_id" not in doc_copy:
                    doc_copy["_id"] = doc_id
                results.append(doc_copy)
            return results
        
        results = []
        for doc_id, doc in self.data.items():
            if self._match_query(doc, query):
                doc_copy = copy.deepcopy(doc)
                if "_id" not in doc_copy:
                    doc_copy["_id"] = doc_id
                results.append(doc_copy)
        return results
    
    def find_one(self, query: Dict):
        """Find single document matching query"""
        if "_id" in query:
            doc = self.data.get(query["_id"])
            return copy.deepcopy(doc) if doc else None
        
        for doc in self.data.values():
            if self._match_query(doc, query):
                return copy.deepcopy(doc)
        return None
    
    def insert_one(self, document: Dict):
        """Insert a single document"""
        doc_id = document.get("_id")
        if doc_id is None:
            raise ValueError("Document must have an _id field")
        self.data[doc_id] = copy.deepcopy(document)
        return type('Result', (), {'inserted_id': doc_id})()
    
    def update_one(self, query: Dict, update: Dict):
        """Update a single document"""
        doc = None
        doc_id = None
        
        if "_id" in query:
            doc_id = query["_id"]
            doc = self.data.get(doc_id)
        else:
            for key, value in self.data.items():
                if self._match_query(value, query):
                    doc_id = key
                    doc = value
                    break
        
        if not doc:
            return type('Result', (), {'modified_count': 0})()
        
        # Handle $push operation
        if "$push" in update:
            for field, value in update["$push"].items():
                if field not in doc:
                    doc[field] = []
                doc[field].append(value)
        
        # Handle $pull operation
        if "$pull" in update:
            for field, value in update["$pull"].items():
                if field in doc and isinstance(doc[field], list):
                    if value in doc[field]:
                        doc[field].remove(value)
        
        # Handle $set operation
        if "$set" in update:
            for field, value in update["$set"].items():
                doc[field] = value
        
        self.data[doc_id] = doc
        return type('Result', (), {'modified_count': 1})()
    
    def count_documents(self, query: Dict):
        """Count documents matching query"""
        if not query:
            return len(self.data)
        
        count = 0
        for doc in self.data.values():
            if self._match_query(doc, query):
                count += 1
        return count
    
    def aggregate(self, pipeline: List[Dict]):
        """Simple aggregation pipeline support"""
        results = list(self.data.values())
        
        for stage in pipeline:
            if "$unwind" in stage:
                field = stage["$unwind"].replace("$", "")
                unwound = []
                for doc in results:
                    value = self._get_nested_field(doc, field)
                    if isinstance(value, list):
                        for item in value:
                            new_doc = copy.deepcopy(doc)
                            self._set_nested_field(new_doc, field, item)
                            unwound.append(new_doc)
                    else:
                        unwound.append(doc)
                results = unwound
            
            elif "$group" in stage:
                group_by = stage["$group"]["_id"]
                if group_by.startswith("$"):
                    field = group_by.replace("$", "")
                    groups = {}
                    for doc in results:
                        value = self._get_nested_field(doc, field)
                        if value not in groups:
                            groups[value] = {"_id": value}
                    results = list(groups.values())
            
            elif "$sort" in stage:
                sort_field = list(stage["$sort"].keys())[0]
                results = sorted(results, key=lambda x: x.get(sort_field, ""))
        
        return results
    
    def _match_query(self, doc: Dict, query: Dict) -> bool:
        """Check if document matches query"""
        for key, value in query.items():
            if key == "_id":
                if doc.get(key) != value:
                    return False
            elif isinstance(value, dict):
                # Handle operators like $in, $gte, $lte
                if "$in" in value:
                    doc_value = self._get_nested_field(doc, key)
                    if not isinstance(doc_value, list):
                        return False
                    # Check if any value in the query matches any value in doc
                    if not any(item in value["$in"] for item in doc_value):
                        return False
                elif "$gte" in value:
                    doc_value = self._get_nested_field(doc, key)
                    if doc_value < value["$gte"]:
                        return False
                elif "$lte" in value:
                    doc_value = self._get_nested_field(doc, key)
                    if doc_value > value["$lte"]:
                        return False
            else:
                if self._get_nested_field(doc, key) != value:
                    return False
        return True
    
    def _get_nested_field(self, doc: Dict, field: str) -> Any:
        """Get nested field value using dot notation"""
        parts = field.split(".")
        value = doc
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        return value
    
    def _set_nested_field(self, doc: Dict, field: str, value: Any):
        """Set nested field value using dot notation"""
        parts = field.split(".")
        current = doc
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

# Create collection objects
activities_collection = InMemoryCollection(activities_data)
teachers_collection = InMemoryCollection(teachers_data)

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]

