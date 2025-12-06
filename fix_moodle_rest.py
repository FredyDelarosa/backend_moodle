#fix_moodle_rest.py
"""
Script para corregir configuración REST en Moodle.
Habilita REST protocol y desactiva restricciones.
"""
import mysql.connector
from mysql.connector import Error
import sys

MOODLE_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "moodle"
}

def connect_db():
    try:
        conn = mysql.connector.connect(**MOODLE_DB_CONFIG)
        print("✓ Conectado a Moodle DB\n")
        return conn
    except Error as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

def execute_query(conn, query, params=None, fetch=False):
    """Ejecuta una query y maneja cursores correctamente"""
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall() if "SELECT" in query.upper() else None
            cursor.close()
            return result
        
        conn.commit()
        cursor.close()
        return True
    except Error as e:
        cursor.close()
        print(f"   ✗ Error SQL: {e}")
        return None

def fix_config_settings(conn):
    """Habilita web services y REST"""
    print("1. Habilitando configuración de web services...")
    
    settings = [
        ("enablewebservices", "1"),
        ("webservice_protocol_rest", "1"),
    ]
    
    for name, value in settings:
        query = "SELECT value FROM mdl_config WHERE name=%s"
        result = execute_query(conn, query, (name,), fetch=True)
        
        if result:
            execute_query(conn, f"UPDATE mdl_config SET value=%s WHERE name=%s", (value, name))
            print(f"   ↻ {name} = {value}")
        else:
            execute_query(conn, f"INSERT INTO mdl_config (name, value) VALUES (%s, %s)", (name, value))
            print(f"   ✓ {name} = {value}")

def add_functions_to_service(conn):
    """Añade funciones al servicio"""
    print("\n2. Añadiendo funciones al servicio API...")
    
    query = "SELECT id FROM mdl_external_services WHERE name='API Service'"
    result = execute_query(conn, query, fetch=True)
    
    if not result:
        print("   ✗ Servicio 'API Service' no encontrado")
        return
    
    service_id = result[0][0]
    
    functions = [
        'core_webservice_get_site_info',
        'core_course_get_courses_by_field',
        'core_course_create_courses',
        'core_user_get_users',
        'core_user_create_users',
        'enrol_manual_enrol_users',
        'core_enrol_get_users_courses',
    ]
    
    for func_name in functions:
        # Verificar si ya está en el servicio
        query = """
            SELECT id FROM mdl_external_services_functions
            WHERE externalserviceid=%s AND functionname=%s
        """
        result = execute_query(conn, query, (service_id, func_name), fetch=True)
        
        if result:
            print(f"   ↻ {func_name}")
        else:
            execute_query(conn, """
                INSERT INTO mdl_external_services_functions 
                (externalserviceid, functionname)
                VALUES (%s, %s)
            """, (service_id, func_name))
            print(f"   ✓ {func_name}")

def disable_service_restrictions(conn):
    """Desactiva restricciones del servicio"""
    print("\n3. Desactivando restricciones del servicio...")
    
    execute_query(conn, """
        UPDATE mdl_external_services 
        SET enabled=1, restrictedusers=0 
        WHERE name='API Service'
    """)
    print("   ✓ Restricciones desactivadas")

def verify_user_permissions(conn):
    """Verifica permisos del usuario admin"""
    print("\n4. Verificando permisos del usuario admin...")
    
    # Obtener ID del usuario admin
    query = "SELECT id FROM mdl_user WHERE username='admin'"
    result = execute_query(conn, query, fetch=True)
    
    if not result:
        print("   ✗ Usuario admin no encontrado")
        return
    
    user_id = result[0][0]
    
    # Obtener contexto del sistema
    query = "SELECT id FROM mdl_context WHERE contextlevel=10 LIMIT 1"
    result = execute_query(conn, query, fetch=True)
    
    if not result:
        print("   ✗ Contexto del sistema no encontrado")
        return
    
    context_id = result[0][0]
    
    # Verificar capacidades
    query = """
        SELECT COUNT(*) FROM mdl_role_assignments 
        WHERE userid=%s AND contextid=%s
    """
    result = execute_query(conn, query, (user_id, context_id), fetch=True)
    
    count = result[0][0] if result else 0
    print(f"   ✓ Usuario admin tiene {count} rol(es) asignado(s)")

def main():
    print("=" * 60)
    print("CORRECCIÓN DE CONFIGURACIÓN REST EN MOODLE")
    print("=" * 60)
    print()
    
    conn = connect_db()
    
    fix_config_settings(conn)
    add_functions_to_service(conn)
    disable_service_restrictions(conn)
    verify_user_permissions(conn)
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✓ CORRECCIONES APLICADAS")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Purga el caché de Moodle:")
    print("   - Site admin → Development → Purge caches")
    print("\n2. Crea un nuevo token (o usa el existente):")
    print("   - Site admin → Plugins → Web services → Manage tokens")
    print("   - Usuario: admin")
    print("   - Service: API Service")
    print("\n3. Copia el token a .env")
    print("4. Ejecuta: python test_moodle_connection.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n✗ Cancelado")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ CORRECCIONES APLICADAS")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Purga el caché de Moodle:")
    print("   - Site admin → Development → Purge caches")
    print("   - O ejecuta desde CLI: php admin/cli/purge_caches.php")
    print("\n2. Crea un nuevo token:")
    print("   - Site admin → Plugins → Web services → Manage tokens")
    print("   - Usuario: admin")
    print("   - Service: API Service")
    print("\n3. Copia el token a .env")
    print("4. Ejecuta: python test_moodle_connection.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n✗ Cancelado")
        sys.exit(1)
