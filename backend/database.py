from pymongo import MongoClient


class Database:

    def __init__(self):

        self.client = MongoClient(
            "mongodb://localhost:27017/",
            serverSelectionTimeoutMS=5000
        )

        self.db = self.client["eduview"]

        self.exam_sessions = self.db["exam_sessions"]

        try:

            self.client.admin.command("ping")

            print("[Database] MongoDB connected successfully")

        except Exception as e:

            print("[Database] MongoDB connection failed:")
            print(e)


    def save_session(self, session):

        result = self.exam_sessions.insert_one(
            session.copy()
        )

        print(
            "[Database] Session saved:",
            session["session_id"]
        )

        return str(result.inserted_id)


    def get_session(self, session_id):

        return self.exam_sessions.find_one(
            {
                "session_id": session_id
            }
        )


    def get_all_sessions(self):

        return list(
            self.exam_sessions.find(
                {},
                {
                    "_id": 0
                }
            ).sort(
                "started_at",
                -1
            )
        )


    def count_sessions(self):

        return self.exam_sessions.count_documents({})


database = Database()