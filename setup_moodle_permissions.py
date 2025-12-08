#setup_moodle_permissions.py
"""
Script para configurar automáticamente los permisos de Moodle.
Requiere acceso directo a la BD de Moodle.

Uso: python setup_moodle_permissions.py
"""
import mysql.connector
from mysql.connector import Error
import sys

# Configuración de conexión a Moodle BD
MOODLE_DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Cambiar si es diferente
    "password": "",  # Cambiar si es diferente
    "database": "moodle"  # Cambiar si es diferente
}

# Capacidades que necesita el rol API Integration
# Capacidades que necesita el rol API Integration
REQUIRED_CAPABILITIES = [
    ("webservice/rest:use", 1),

    # Cursos: lectura + búsqueda + listado
    ("moodle/course:view", 1),
    ("moodle/course:viewhiddencourses", 1),
    ("moodle/course:viewparticipants", 1),
    ("moodle/category:viewhiddencategories", 1),
    ("moodle/category:manage", 1),
    ("moodle/course:update", 1),
    ("moodle/course:create", 1),

    # Acceso a funciones core_course_get_courses y get_courses_by_field
    ("moodle/course:viewdetails", 1),

    # Usuarios
    ("moodle/user:create", 1),
    ("moodle/user:update", 1),

    # Enrolamiento
    ("moodle/role:assign", 1),
    ("enrol/manual:manage", 1),
    ("enrol/manual:enrol", 1),
    ("enrol/manual:unenrol", 1),
]



def connect_to_moodle_db():
    """Conecta a la base de datos de Moodle"""
    try:
        conn = mysql.connector.connect(**MOODLE_DB_CONFIG)
        print("✓ Conectado a Moodle DB")
        return conn
    except Error as e:
        print(f"✗ Error de conexión: {e}")
        sys.exit(1)


def create_api_role(conn):
    """Crea el rol 'API Integration' en Moodle"""
    cursor = conn.cursor()
    
    try:
        # Verificar si el rol ya existe
        cursor.execute("SELECT id FROM mdl_role WHERE shortname='apiintegration'")
        existing = cursor.fetchone()
        
        if existing:
            print(f"✓ Rol 'apiintegration' ya existe (ID: {existing[0]})")
            return existing[0]
        
        # Crear rol
        print("\nCreando rol 'API Integration'...")
        cursor.execute("""
            INSERT INTO mdl_role (name, shortname, description, archetype)
            VALUES ('API Integration', 'apiintegration', 'Rol para integración con API', 'none')
        """)
        conn.commit()
        
        role_id = cursor.lastrowid
        print(f"✓ Rol creado con ID: {role_id}")
        
        return role_id
        
    except Error as e:
        print(f"✗ Error creando rol: {e}")
        sys.exit(1)
    finally:
        cursor.close()


def assign_capabilities_to_role(conn, role_id):
    """Asigna capacidades al rol"""
    cursor = conn.cursor()
    
    try:
        print(f"\nAsignando capacidades al rol {role_id}...")
        
        # Obtener ID del contexto del sistema (generalmente 1)
        cursor.execute("SELECT id FROM mdl_context WHERE contextlevel=10 LIMIT 1")
        context = cursor.fetchone()
        if not context:
            print("✗ No se encontró contexto del sistema")
            sys.exit(1)
        
        context_id = context[0]
        
        for capability, permission in REQUIRED_CAPABILITIES:
            try:
                # Verificar si ya existe
                cursor.execute("""
                    SELECT id FROM mdl_role_capabilities
                    WHERE roleid=%s AND capability=%s AND contextid=%s
                """, (role_id, capability, context_id))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Actualizar
                    cursor.execute("""
                        UPDATE mdl_role_capabilities
                        SET permission=%s
                        WHERE roleid=%s AND capability=%s AND contextid=%s
                    """, (permission, role_id, capability, context_id))
                    print(f"  ↻ {capability}")
                else:
                    # Insertar
                    cursor.execute("""
                        INSERT INTO mdl_role_capabilities (contextid, roleid, capability, permission)
                        VALUES (%s, %s, %s, %s)
                    """, (context_id, role_id, capability, permission))
                    print(f"  ✓ {capability}")
                
            except Error as e:
                print(f"  ✗ {capability}: {e}")
        
        conn.commit()
        print("✓ Capacidades asignadas")
        
    except Error as e:
        print(f"✗ Error asignando capacidades: {e}")
        sys.exit(1)
    finally:
        cursor.close()


def assign_role_to_user(conn, role_id, username):
    """Asigna el rol a un usuario específico"""
    cursor = conn.cursor()
    
    try:
        # Obtener ID del usuario
        cursor.execute("SELECT id FROM mdl_user WHERE username=%s", (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"\n✗ Usuario '{username}' no encontrado")
            return False
        
        user_id = user[0]
        
        # Obtener contexto del sistema
        cursor.execute("SELECT id FROM mdl_context WHERE contextlevel=10 LIMIT 1")
        context = cursor.fetchone()
        context_id = context[0]
        
        # Verificar si ya tiene el rol
        cursor.execute("""
            SELECT id FROM mdl_role_assignments
            WHERE roleid=%s AND userid=%s AND contextid=%s
        """, (role_id, user_id, context_id))
        
        existing = cursor.fetchone()
        
        if existing:
            print(f"✓ Usuario '{username}' ya tiene el rol")
            return True
        
        # Asignar rol
        cursor.execute("""
            INSERT INTO mdl_role_assignments (roleid, userid, contextid, timemodified, modifierid)
            VALUES (%s, %s, %s, NOW(), 2)
        """, (role_id, user_id, context_id))
        
        conn.commit()
        print(f"✓ Rol asignado al usuario '{username}'")
        
        return True
        
    except Error as e:
        print(f"✗ Error asignando rol al usuario: {e}")
        return False
    finally:
        cursor.close()


def enable_webservices(conn):
    """Habilita web services en Moodle"""
    cursor = conn.cursor()
    
    try:
        print("\nHabilitando web services...")
        
        settings = [
            ("enablewebservices", "1"),
            ("enabledebugdb", "0"),
        ]
        
        for name, value in settings:
            cursor.execute("""
                SELECT id FROM mdl_config WHERE name=%s
            """, (name,))
            
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("""
                    UPDATE mdl_config SET value=%s WHERE name=%s
                """, (value, name))
                print(f"  ↻ {name} = {value}")
            else:
                cursor.execute("""
                    INSERT INTO mdl_config (name, value)
                    VALUES (%s, %s)
                """, (name, value))
                print(f"  ✓ {name} = {value}")
        
        conn.commit()
        print("✓ Web services habilitado")
        
    except Error as e:
        print(f"✗ Error habilitando web services: {e}")
        return False
    finally:
        cursor.close()
    
    return True


def create_web_service(conn):
    """Crea un servicio web personalizado"""
    cursor = conn.cursor()
    
    try:
        print("\nCreando servicio web 'API Service'...")
        
        # Verificar si ya existe
        cursor.execute("SELECT id FROM mdl_external_services WHERE name='API Service'")
        existing = cursor.fetchone()
        
        if existing:
            print(f"✓ Servicio 'API Service' ya existe (ID: {existing[0]})")
            return existing[0]
        
        # Crear servicio
        cursor.execute("""
            INSERT INTO mdl_external_services 
            (name, enabled, requiredcapability, restrictedusers, shortname, component)
            VALUES ('API Service', 1, '', 1, 'apiservice', 'moodle')
        """)
        conn.commit()
        
        service_id = cursor.lastrowid
        print(f"✓ Servicio creado con ID: {service_id}")
        
        return service_id
        
    except Error as e:
        print(f"✗ Error creando servicio: {e}")
        return None
    finally:
        cursor.close()


def add_user_to_service(conn, service_id, user_id):
    """Añade un usuario al servicio web"""
    cursor = conn.cursor()
    
    try:
        # Verificar si ya existe
        cursor.execute("""
            SELECT id FROM mdl_external_services_users
            WHERE externalserviceid=%s AND userid=%s
        """, (service_id, user_id))
        
        existing = cursor.fetchone()
        
        if existing:
            print(f"✓ Usuario ya está en el servicio")
            return True
        
        cursor.execute("""
            INSERT INTO mdl_external_services_users (externalserviceid, userid, timecreated)
            VALUES (%s, %s, NOW())
        """, (service_id, user_id))
        
        conn.commit()
        print(f"✓ Usuario añadido al servicio")
        
        return True
        
    except Error as e:
        print(f"✗ Error añadiendo usuario al servicio: {e}")
        return False
    finally:
        cursor.close()


def main():
    print("=" * 60)
    print("CONFIGURACIÓN AUTOMÁTICA DE PERMISOS MOODLE")
    print("=" * 60)
    
    # Datos a configurar
    username = input("\nIngresa el usuario de Moodle para el token: ").strip() or "admin"
    
    print(f"\nConfigurando permisos para usuario: {username}")
    print(f"BD de Moodle: {MOODLE_DB_CONFIG['database']}")
    print()
    
    # Conectar
    conn = connect_to_moodle_db()
    
    # Crear rol
    role_id = create_api_role(conn)
    
    # Asignar capacidades
    assign_capabilities_to_role(conn, role_id)
    
    # Asignar rol al usuario
    if not assign_role_to_user(conn, role_id, username):
        print("\n✗ No se pudo asignar el rol al usuario")
        conn.close()
        sys.exit(1)
    
    # Habilitar web services
    if not enable_webservices(conn):
        print("\n✗ No se pudo habilitar web services")
        conn.close()
        sys.exit(1)
    
    # Crear servicio web
    service_id = create_web_service(conn)
    
    if service_id:
        # Obtener ID del usuario
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM mdl_user WHERE username=%s", (username,))
        user_result = cursor.fetchone()
        cursor.close()
        
        if user_result:
            user_id = user_result[0]
            add_user_to_service(conn, service_id, user_id)
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✓ CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\nPasos siguientes:")
    print("1. Crea un token en Moodle:")
    print("   - Site admin → Plugins → Web services → Manage tokens")
    print("   - Usuario: " + username)
    print("   - Service: API Service")
    print("2. Copia el token a tu archivo .env")
    print("3. Ejecuta: python test_moodle_connection.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Operación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error no esperado: {e}")
        sys.exit(1)
