from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response
import jwt
from managers.users import authenticate_user, get_user_current
from models import User, Course, Certificate, Processe, Passed
import asyncpg
from schemas import UserAllInfo, UserGet, UserAuth, UserEdit, OrgAllInfo, CreateCourse, \
    AddMyCourse, CertificateAllInfo, CheckEmail, CheckAnswer
from passlib.hash import bcrypt
import ormar


JWT_SECRET = 'myjwtsecret'

router = APIRouter(
    prefix=""
)


@router.post('/')
async def auth(data: UserAuth):
    user = await authenticate_user(data.username, data.password_hash)
    if not user:
        return {'error': 'invaid credentials'}
    user = UserGet(
        id=str(user.id),
        username=user.username,
        password_hash=user.password_hash
    )
    token = jwt.encode(user.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/reg_user')
async def register(user: UserAllInfo):
    try:
        user.password_hash = bcrypt.hash(user.password_hash)
        user_dict = user.dict()
        await User.objects.create(**user_dict)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User already exists")
    return Response(status_code=200, content="User created")


@router.post('/reg_org')
async def register_org(org: OrgAllInfo):
    try:
        org.password_hash = bcrypt.hash(org.password_hash)
        user_dict = org.dict()
        await User.objects.create(**user_dict)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User already exists")
    return Response(status_code=200, content="User created")


@router.post('/check_username')
async def check_username(username: CheckEmail):
    try:
        await User.objects.get(username=username.username)
        return CheckAnswer(answer=False)
    except ormar.exceptions.NoMatch:
        return CheckAnswer(answer=True)


@router.patch('/me')
async def user_edit(new_user: UserEdit, user=Depends(get_user_current)):
    if new_user.password_hash:
        new_user.password_hash = bcrypt.hash(new_user.password_hash)
    user = await User.objects.get(id=user.id)
    try:
        await user.update(**{k: v for k, v in new_user.dict().items() if v})
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="Nickname is already in use")
    return user


@router.get('/me')
async def get_me(user=Depends(get_user_current)):
    user_get = await User.objects.get(id=user.id)
    return user_get


@router.post('/create_course')
async def create_course(course: CreateCourse, user=Depends(get_user_current)):
    if user.is_organization:
        course.organization = user.name
        await Course.objects.create(**course.dict())
        return "Course created"
    else:
        return Response(status_code=403)


@router.delete('/delete_courses/{courses_id}')
async def delete_courses(courses_id: UUID, user=Depends(get_user_current)):
    if user.is_organization:
        courses = await Course.objects.get(id=courses_id)
        await courses.delete()
        return Response(status_code=200, content="Course deleted")
    return Response(status_code=404, content="User is not organization")


@router.get('/courses')
async def get_all_courses():
    courses = await Course.objects.all()
    return courses


@router.get('/courses/{course_id}')
async def get_course_by_id(course_id: UUID):
    course = await Course.objects.get(id=course_id)
    return course


@router.post('/courses/{course_id}')
async def add_my_course(course_id: UUID, user=Depends(get_user_current)):
    await Processe.objects.create(**(AddMyCourse(user_id=user.id, course_id=course_id)).dict())
    return 'all ok'


@router.get('/my_courses')
async def get_my_courses(user=Depends(get_user_current)):
    my_courses = await Processe.objects.filter(user_id=user.id).all()
    courses = []
    for i in my_courses:
        course = await Course.objects.get(id=i.course_id)
        courses.append(course)
    return courses


@router.post('/courses/{course_id}/passed_course')
async def passed_course(course_id: UUID, user=Depends(get_user_current)):
    course = await Course.objects.get(id=course_id)
    if course.is_certificate:
        await Certificate.objects.create(
            **(CertificateAllInfo(user_id=user.id, name=course.name, link=course.link)).dict())
    await Passed.objects.create(**(AddMyCourse(user_id=user.id, course_id=course_id)).dict())
    return Response(status_code=200, content="all ok")


@router.get('/my_passed_courses')
async def get_passed_courses(user=Depends(get_user_current)):
    passed_courses = await Passed.objects.filter(user_id=user.id).all()
    return passed_courses


@router.delete('/delete_my_passed_courses/{courses_id}')
async def delete_passed_courses(courses_id: UUID, user=Depends(get_user_current)):
    if not user.is_organization:
        passed_courses = await Passed.objects.filter(user_id=courses_id).all()
        await passed_courses.delete()
        return Response(status_code=200, content="Course is not passed")
    return Response(status_code=404, content="User is organization")


@router.get('/my_certificates')
async def get_certificates(user=Depends(get_user_current)):
    certificates = await Certificate.objects.filter(user_id=user.id).all()
    return certificates
