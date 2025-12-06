class MoodleService:
    def __init__(self, moodle_client):
        self.moodle = moodle_client

    async def course_exists(self, shortname: str):
        return await self.moodle.get_course_by_shortname(shortname)

    async def user_exists(self, email: str):
        return await self.moodle.get_user_by_email(email)

    async def get_user_courses(self, userid: int):
        return await self.moodle.get_user_courses(userid)

    async def create_course(self, fullname: str, shortname: str):
        return await self.moodle.create_course(fullname, shortname)

    async def create_user(self, username: str, firstname: str, lastname: str, email: str):
        return await self.moodle.create_user(username, firstname, lastname, email)
