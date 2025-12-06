# API Endpoints - Backend Moodle

**Base URL**: `http://localhost:8000`  
**Documentación interactiva**: `/docs` (Swagger) o `/redoc` (ReDoc)

---

## 📚 Estructura de Rutas

Todas las rutas están bajo el prefijo `/api`.

---

## 1. ACADEMY - Gestión Académica

### 1.1 Programas de Estudio

**POST** `/api/programas` - Crear programa
```json
{
  "nombre": "Ingeniería de Software",
  "numero_cuatrimestres": 8
}
```

**GET** `/api/programas` - Listar todos los programas

**GET** `/api/programas/{pid}` - Obtener programa por ID

**PUT** `/api/programas/{pid}` - Actualizar programa
```json
{
  "nombre": "Ingeniería de Software Actualizado",
  "numero_cuatrimestres": 9
}
```

**DELETE** `/api/programas/{pid}` - Eliminar programa

---

### 1.2 Cuatrimestres

**POST** `/api/cuatrimestres` - Crear cuatrimestre
```json
{
  "numero": 1,
  "programa_id": 1
}
```

**GET** `/api/cuatrimestres` - Listar cuatrimestres con programa asociado

**PUT** `/api/cuatrimestres/{cid}` - Actualizar cuatrimestre
```json
{
  "numero": 1,
  "programa_id": 1
}
```

**DELETE** `/api/cuatrimestres/{cid}` - Eliminar cuatrimestre

---

### 1.3 Asignaturas

**POST** `/api/asignaturas` - Crear asignatura
```json
{
  "nombre": "Programación Orientada a Objetos",
  "cuatrimestre_id": 1,
  "codigo": "CS101"
}
```

**GET** `/api/asignaturas` - Listar asignaturas con cuatrimestre

**PUT** `/api/asignaturas/{aid}` - Actualizar asignatura
```json
{
  "nombre": "POO Avanzado",
  "cuatrimestre_id": 1,
  "codigo": "CS101"
}
```

**DELETE** `/api/asignaturas/{aid}` - Eliminar asignatura

---

### 1.4 Docentes

**POST** `/api/docentes` - Crear docente (✅ **NO depende de otros**)
```json
{
  "nombre": "Dr. Juan García",
  "correo": "juan.garcia@uni.edu"
}
```

**GET** `/api/docentes` - Listar docentes

**PUT** `/api/docentes/{did}` - Actualizar docente
```json
{
  "nombre": "Dr. Juan García López",
  "correo": "juan.garcia.lopez@uni.edu"
}
```

**DELETE** `/api/docentes/{did}` - Eliminar docente

---

### 1.5 Docente-Asignatura (Relación)

**POST** `/api/docente-asignatura` - Asignar docente a una asignatura
```json
{
  "docente_id": 1,
  "asignatura_id": 5
}
```

**GET** `/api/docente-asignatura` - Listar relaciones docente-asignatura

---

### 1.6 Alumnos

**POST** `/api/alumnos` - Crear alumno (✅ **NO depende de otros**)
```json
{
  "nombre": "Carlos López",
  "matricula": "2025001",
  "cuatrimestre": 1,
  "correo": "carlos.lopez@uni.edu"
}
```

**GET** `/api/alumnos` - Listar alumnos

**PUT** `/api/alumnos/{aid}` - Actualizar alumno
```json
{
  "nombre": "Carlos López Martínez",
  "matricula": "2025001",
  "cuatrimestre": 2,
  "correo": "carlos.lopez@uni.edu"
}
```

**DELETE** `/api/alumnos/{aid}` - Eliminar alumno

---

### 1.7 Grupos

**POST** `/api/grupos` - Crear grupo
```json
{
  "nombre": "Grupo A",
  "asignatura_id": 5,
  "docente_id": 1,
  "cuatrimestre_id": 1,
  "capacidad": 30
}
```

**GET** `/api/grupos` - Listar grupos con asignatura y docente

**PUT** `/api/grupos/{gid}` - Actualizar grupo
```json
{
  "nombre": "Grupo A - Turno Mañana",
  "asignatura_id": 5,
  "docente_id": 1,
  "cuatrimestre_id": 1,
  "capacidad": 35
}
```

**DELETE** `/api/grupos/{gid}` - Eliminar grupo

**POST** `/api/grupos/{gid}/alumnos` - Añadir alumno al grupo
```json
{
  "alumno_id": 10
}
```

**GET** `/api/grupos/{gid}/alumnos` - Listar alumnos del grupo

**DELETE** `/api/grupos/{gid}/alumnos/{aid}` - Remover alumno del grupo

---

## 2. SYNC - Sincronización con Moodle

**POST** `/api/sync/group` - Sincronizar un grupo con Moodle
```json
{
  "grupo_id": 1,
  "createIfMissing": true,
  "concurrencyLimit": 5
}
```

**Respuesta** (ejemplo):
```json
{
  "course": {
    "shortname": "P1_C1_A5_G1",
    "id": 2
  },
  "teacher": {
    "id": 3,
    "nombre": "Dr. Juan García"
  },
  "students": [
    {
      "alumno_id": 10,
      "moodle_id": 100,
      "status": "ok",
      "existed": false
    }
  ],
  "errors": []
}
```

---

## 3. MOODLE - Operaciones Directas en Moodle

**GET** `/api/moodle/course/exists/{shortname}` - Verificar si curso existe

**POST** `/api/moodle/course` - Crear curso en Moodle
```json
{
  "fullname": "Mi Curso",
  "shortname": "mi_curso_001"
}
```

**GET** `/api/moodle/user/exists/{email}` - Verificar si usuario existe

**POST** `/api/moodle/user` - Crear usuario en Moodle
```json
{
  "username": "juanperez",
  "firstname": "Juan",
  "lastname": "Pérez",
  "email": "juan.perez@example.com"
}
```

**GET** `/api/moodle/user/{userid}/courses` - Obtener cursos del usuario

---

## 📋 Orden de Creación Recomendado

1. **Programas** (`POST /api/programas`)
2. **Docentes** (`POST /api/docentes`)
3. **Alumnos** (`POST /api/alumnos`)
4. **Cuatrimestres** (`POST /api/cuatrimestres`)
5. **Asignaturas** (`POST /api/asignaturas`)
6. **Docente-Asignatura** (`POST /api/docente-asignatura`)
7. **Grupos** (`POST /api/grupos`)
8. **Alumnos-Grupo** (`POST /api/grupos/{gid}/alumnos`)
9. **Sync** (`POST /api/sync/group`)

---

## 🔄 Flujo Típico

```
1. Crear programa
   ↓
2. Crear cuatrimestre (asociado a programa)
   ↓
3. Crear asignatura (asociada a cuatrimestre)
   ↓
4. Crear docente
   ↓
5. Asociar docente a asignatura
   ↓
6. Crear grupo (asociado a asignatura + docente + cuatrimestre)
   ↓
7. Crear alumnos
   ↓
8. Agregar alumnos al grupo
   ↓
9. Sincronizar grupo con Moodle (crea curso, usuarios y enrollments)
```

---

## 📊 Dependencias de Tablas

```
programa_estudio (independiente)
    ↓
cuatrimestre (FK: programa_id)
    ↓
asignatura (FK: cuatrimestre_id)
    ↓
docente_asignatura (FK: docente_id, asignatura_id)
    ↓
grupo (FK: asignatura_id, docente_id, cuatrimestre_id)
    ↓
grupo_alumno (FK: grupo_id, alumno_id)

docente (independiente)
alumno (independiente, campo cuatrimestre es solo número)
```

---

## ✅ Endpoints que NO Dependen de Otros

- **POST** `/api/programas` - Crear programa
- **POST** `/api/docentes` - Crear docente
- **POST** `/api/alumnos` - Crear alumno

Todos los demás requieren IDs de otras entidades.

---

## 🧪 Ejemplo de Uso Completo

```bash
# 1. Crear programa
curl -X POST "http://localhost:8000/api/programas" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ingeniería","numero_cuatrimestres":8}'

# 2. Crear docente
curl -X POST "http://localhost:8000/api/docentes" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Dr. García","correo":"garcia@uni.edu"}'

# 3. Crear alumno
curl -X POST "http://localhost:8000/api/alumnos" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan López","matricula":"2025001","cuatrimestre":1,"correo":"juan@uni.edu"}'

# 4. Crear cuatrimestre (requiere programa_id)
curl -X POST "http://localhost:8000/api/cuatrimestres" \
  -H "Content-Type: application/json" \
  -d '{"numero":1,"programa_id":1}'

# ... etc
```

---

## 📌 Notas Importantes

- Todos los endpoints requieren que **la BD esté inicializada** (`python db/init_db.sql`)
- El endpoint `/api/sync/group` sincroniza con Moodle automáticamente
- Los IDs se generan automáticamente en la BD
- Las fechas usan formato `datetime` de MySQL
- La concurrencia en sync se controla con `concurrencyLimit`

