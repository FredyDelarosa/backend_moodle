from fastapi import APIRouter
from moodle.client import get_moodle_client
from moodle.service import MoodleService
from pydantic import BaseModel

router = APIRouter(prefix="/api/moodle", tags=["Moodle"])

class CreateUserRequest(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str

class CreateCourseRequest(BaseModel):
    fullname: str
    shortname: str


@router.get("/course/exists/{shortname}")
async def course_exists(shortname: str):
    moodle = get_moodle_client()
    service = MoodleService(moodle)
    return await service.course_exists(shortname)


@router.get("/user/exists/{email}")
async def user_exists(email: str):
    moodle = get_moodle_client()
    service = MoodleService(moodle)
    return await service.user_exists(email)


@router.get("/user/{userid}/courses")
async def user_courses(userid: int):
    moodle = get_moodle_client()
    service = MoodleService(moodle)
    return await service.get_user_courses(userid)


@router.post("/course")
async def create_course(request: CreateCourseRequest):
    moodle = get_moodle_client()
    service = MoodleService(moodle)
    return await service.create_course(request.fullname, request.shortname)


@router.post("/user")
async def create_user(request: CreateUserRequest):
    moodle = get_moodle_client()
    service = MoodleService(moodle)
    return await service.create_user(
        request.username,
        request.firstname,
        request.lastname,
        request.email
    )
