import asyncio
from typing import Optional
from core.config import settings
import httpx

class MockMoodleClient:
    def __init__(self, delay: float = 0.08):
        self.delay = delay
        self._courses = {}
        self._users = {}
        self._next_course_id = 1000
        self._next_user_id = 5000
        self._enrolments = {}

    async def get_site_info(self):
        await asyncio.sleep(self.delay)
        return {"sitename": "Moodle Mock", "username": "mock"}
    
    async def get_courses(self):
        await asyncio.sleep(self.delay)
        return list(self._courses.values())

    async def get_course_by_shortname(self, shortname: str):
        await asyncio.sleep(self.delay)
        c = self._courses.get(shortname)
        return {"courses": [c]} if c else {"courses": []}

    async def create_course(self, fullname: str, shortname: str, categoryid: int = 1):
        await asyncio.sleep(self.delay)
        if shortname in self._courses:
            return [{"id": self._courses[shortname]["id"]}]
        cid = self._next_course_id
        self._next_course_id += 1
        self._courses[shortname] = {"id": cid, "fullname": fullname, "shortname": shortname}
        self._enrolments[cid] = set()
        return [{"id": cid}]

    async def get_user_by_email(self, email: str):
        await asyncio.sleep(self.delay)
        for u in self._users.values():
            if u.get("email") == email:
                return {"users": [u]}
        return {"users": []}

    async def get_user_courses(self, userid: int):
        await asyncio.sleep(self.delay)
        courses = []
        for cid, enrollments in self._enrolments.items():
            if userid in enrollments:
                for c in self._courses.values():
                    if c["id"] == cid:
                        courses.append(c)
        return courses

    async def create_user(self, username: str, firstname: str, lastname: str, email: str, password: str = "Password123!"):
        await asyncio.sleep(self.delay)
        key = email or username
        if key in self._users:
            return [{"id": self._users[key]["id"]}]
        uid = self._next_user_id
        self._next_user_id += 1
        self._users[key] = {"id": uid, "username": username, "email": email, "firstname": firstname, "lastname": lastname}
        return [{"id": uid}]

    async def enrol_user(self, userid: int, courseid: int, roleid: int = 5):
        await asyncio.sleep(self.delay)
        if courseid not in self._enrolments:
            self._enrolments[courseid] = set()
        self._enrolments[courseid].add(userid)
        return {"status": "ok"}
    
    async def update_course(self, courseid: int, fullname: str, shortname: str):
        await asyncio.sleep(self.delay)
        for key, c in list(self._courses.items()):
            if c["id"] == courseid:
                c["fullname"] = fullname
                c["shortname"] = shortname
                if key != shortname:
                    self._courses.pop(key)
                    self._courses[shortname] = c
                return {"status": "ok"}
        return {"status": "not_found"}
    
    async def delete_course(self, courseid: int):
        await asyncio.sleep(self.delay)
        for key, c in list(self._courses.items()):
            if c["id"] == courseid:
                self._courses.pop(key)
                if courseid in self._enrolments:
                    self._enrolments.pop(courseid)
                return {"status": "ok"}
        return {"status": "not_found"}



class MoodleHttpClient:
    def __init__(self, base_url: str, token: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.endpoint = f"{self.base_url}/webservice/rest/server.php"
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=self.timeout)

    async def _post(self, func: str, params: dict):
        payload = {"wstoken": self.token, "moodlewsrestformat": "json", "wsfunction": func}
        payload.update(params)
        r = await self._client.post(self.endpoint, data=payload)
        r.raise_for_status()
        data = r.json()
        # Detectar errores de Moodle en la respuesta
        if isinstance(data, dict) and "exception" in data:
            error_msg = data.get("message", data.get("exception", "Unknown error"))
            raise Exception(f"Moodle error: {error_msg}")
        return data

    async def get_courses(self):
        return await self._post("core_course_get_courses_by_field", {
    "field": "shortname",
    "value": "CONC-A"
})

    
    async def get_site_info(self):
        return await self._post("core_webservice_get_site_info", {})

    async def get_course_by_shortname(self, shortname: str):
        return await self._post("core_course_get_courses_by_field", {"field": "shortname", "value": shortname})

    async def create_course(self, fullname: str, shortname: str, categoryid: int = 1):
        params = { "courses[0][fullname]": fullname, "courses[0][shortname]": shortname, "courses[0][categoryid]": categoryid }
        return await self._post("core_course_create_courses", params)

    async def get_user_by_email(self, email: str):
        return await self._post("core_user_get_users", {"criteria[0][key]": "email", "criteria[0][value]": email})

    async def create_user(self, username: str, firstname: str, lastname: str, email: str, password: str = "Password123!"):
        params = {
            "users[0][username]": username,
            "users[0][firstname]": firstname,
            "users[0][lastname]": lastname,
            "users[0][email]": email,
            "users[0][password]": password
        }
        return await self._post("core_user_create_users", params)

    async def enrol_user(self, userid: int, courseid: int, roleid: int = 5):
        params = {
            "enrolments[0][roleid]": roleid,
            "enrolments[0][userid]": userid,
            "enrolments[0][courseid]": courseid
        }
        return await self._post("enrol_manual_enrol_users", params)

    async def get_user_courses(self, userid: int):
        return await self._post("core_enrol_get_users_courses", {"userid": userid})

    async def close(self):
        await self._client.aclose()

    async def update_course(self, courseid: int, fullname: str, shortname: str):
        params = {
            "courses[0][id]": courseid,
            "courses[0][fullname]": fullname,
            "courses[0][shortname]": shortname
        }
        return await self._post("core_course_update_courses", params)
    
    async def delete_course(self, courseid: int):
        params = { "courseids[0]": courseid }
        return await self._post("core_course_delete_courses", params)


def get_moodle_client():
    if settings.moodle_token:
        return MoodleHttpClient(settings.moodle_url, settings.moodle_token)
    return MockMoodleClient()

