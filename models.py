class Activity:
    """
    A class to represent an Activity notification.
    ...

    Attributes
    ----------
    event_id : str
        id of the corresponding event
    user_id : str
        id of the corresponding user
    activity_time : int
        time of the activity
    activity_type : str
        type of activity
    activity_data : str
        data about the activity

    """

    def __init__(self, event_id: str, user_id: str, activity_time: int, activity_type: str, activity_data: str):

        assert event_id != "", "Event ID cannot be empty"
        assert user_id != "", "User ID cannot be empty"
        assert type(activity_time) == int and activity_time > 0, "Activity Time must be an integer and greater than zero"
        assert activity_type != "", "Activity Type cannot be empty"
        assert activity_data != "", "Activity Data cannot be empty"
        
        self.event_id = event_id
        self.user_id = user_id
        self.activity_time = activity_time
        self.activity_type = activity_type
        self.activity_data = activity_data


        