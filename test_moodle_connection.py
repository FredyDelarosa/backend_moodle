#test_moodle_connection.py
"""
Test rápido para validar la configuración del cliente Moodle.
Uso: python test_moodle_connection.py
"""
import asyncio
from moodle.client import get_moodle_client, MoodleHttpClient, MockMoodleClient
from core.config import settings


async def test_http_client():
    """Test conexión real a Moodle HTTP"""
    print("\n=== TEST: MoodleHttpClient (Real) ===")
    try:
        client = MoodleHttpClient(settings.moodle_url, settings.moodle_token)
        
        # Test 1: Site info
        print("\n1. Testeando get_site_info()...")
        info = await client.get_site_info()
        print(f"✓ Sitio: {info.get('sitename', 'N/A')}")
        print(f"✓ Usuario: {info.get('username', 'N/A')}")
        
        # Test 2: Create course
        print("\n2. Testeando create_course()...")
        course = await client.create_course("Test Course", "test_course_001", categoryid=1)
        print(f"✓ Curso creado con ID: {course[0].get('id', 'N/A')}")
        
        # Test 3: Get course by shortname
        print("\n3. Testeando get_course_by_shortname()...")
        found = await client.get_course_by_shortname("test_course_001")
        print(f"✓ Cursos encontrados: {len(found.get('courses', []))}")
        
        # Test 4: Create user
        print("\n4. Testeando create_user()...")
        user = await client.create_user("testuser001", "Test", "User", "testuser001@example.com")
        print(f"✓ Usuario creado con ID: {user[0].get('id', 'N/A')}")
        
        # Test 5: Get user by email
        print("\n5. Testeando get_user_by_email()...")
        found_user = await client.get_user_by_email("testuser001@example.com")
        print(f"✓ Usuarios encontrados: {len(found_user.get('users', []))}")
        
        # Test 6: Get user courses
        print("\n6. Testeando get_user_courses()...")
        uid = user[0].get('id')
        courses = await client.get_user_courses(uid)
        print(f"✓ Cursos del usuario: {len(courses) if isinstance(courses, list) else 'N/A'}")
        
        # Test 7: Enrol user
        print("\n7. Testeando enrol_user()...")
        courseid = course[0].get('id')
        enrol = await client.enrol_user(uid, courseid, roleid=5)
        print(f"✓ Enrolado correctamente")
        
        await client.close()
        print("\n✓ Todos los tests PASARON")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False
    
    return True


async def test_mock_client():
    """Test cliente mock"""
    print("\n\n=== TEST: MockMoodleClient ===")
    try:
        client = MockMoodleClient()
        
        # Test 1: Site info
        print("\n1. Testeando get_site_info()...")
        info = await client.get_site_info()
        print(f"✓ Sitio: {info.get('sitename', 'N/A')}")
        
        # Test 2: Create course
        print("\n2. Testeando create_course()...")
        course = await client.create_course("Mock Course", "mock_course_001")
        print(f"✓ Curso creado con ID: {course[0].get('id', 'N/A')}")
        
        # Test 3: Create user
        print("\n3. Testeando create_user()...")
        user = await client.create_user("mockuser001", "Mock", "User", "mockuser001@example.com")
        print(f"✓ Usuario creado con ID: {user[0].get('id', 'N/A')}")
        
        # Test 4: Get user courses (vacío antes de enrolarse)
        print("\n4. Testeando get_user_courses() (antes de enrolarse)...")
        uid = user[0].get('id')
        courses_before = await client.get_user_courses(uid)
        print(f"✓ Cursos antes: {len(courses_before)}")
        
        # Test 5: Enrol user
        print("\n5. Testeando enrol_user()...")
        courseid = course[0].get('id')
        await client.enrol_user(uid, courseid)
        print(f"✓ Usuario enrollado")
        
        # Test 6: Get user courses (después de enrolarse)
        print("\n6. Testeando get_user_courses() (después de enrolarse)...")
        courses_after = await client.get_user_courses(uid)
        print(f"✓ Cursos después: {len(courses_after)}")
        
        print("\n✓ Todos los tests PASARON")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False
    
    return True


async def main():
    print("=" * 50)
    print("VALIDACIÓN DE CONFIGURACIÓN MOODLE")
    print("=" * 50)
    
    # Determinar qué cliente usar
    if settings.moodle_token and settings.moodle_token != "default":
        print(f"\nModo: HTTP REAL")
        print(f"URL: {settings.moodle_url}")
        print(f"Token: {settings.moodle_token[:10]}...")
        result = await test_http_client()
    else:
        print(f"\nModo: MOCK (sin token real configurado)")
        result = await test_mock_client()
    
    if not result:
        print("\n✗ VALIDACIÓN FALLIDA")
        exit(1)
    else:
        print("\n✓ VALIDACIÓN EXITOSA")


if __name__ == "__main__":
    asyncio.run(main())
