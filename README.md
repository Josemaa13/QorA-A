# QorA-A

QorA-A es una plataforma moderna de red social y publicaciones de alto rendimiento, construida con una robusta arquitectura de persistencia políglota (Polyglot Persistence). Utiliza diferentes tecnologías de bases de datos para gestionar necesidades de datos específicas de manera eficiente, desde relaciones complejas entre usuarios hasta análisis en tiempo real.

## 🚀 Características

### 👤 Gestión de Usuarios
- **Autenticación y Perfiles**: Registro seguro de usuarios, inicio de sesión y personalización de perfiles.
- **Relaciones entre Usuarios**: Mecanismos de Seguir/Dejar de seguir gestionados mediante estructuras de grafos para un rendimiento óptimo.

### 📝 Publicaciones
- **Creación de Contenido**: Publicación de contenido enriquecido con soporte para archivos multimedia.
- **Gestión de Multimedia**: Manejo eficiente de documentos e imágenes subidos por los usuarios.
- **Gestión de Temas**: Sistema de categorización de contenido mediante temas, permitiendo a los administradores gestionar temas y a los usuarios asignarlos a documentos.

### 🤖 Recomendaciones
- **Motor Basado en Grafos**: Utiliza Neo4j para proporcionar sugerencias de alta relevancia para usuarios y contenido, basadas en la topología de la red y los intereses comunes.

### 🔔 Notificaciones
- **Alertas en Tiempo Real**: Actualizaciones instantáneas sobre actividades de los usuarios, interacciones y anuncios del sistema.
- **Entrega Escalable**: Almacenamiento y recuperación de notificaciones optimizados.

### 📊 Análisis (Analytics)
- **Seguimiento de Actividad**: Monitoreo exhaustivo del compromiso del usuario y el rendimiento del sistema.
- **Panel de Control (Dashboard)**: Perspectivas visuales sobre el crecimiento de la plataforma y la popularidad del contenido, impulsadas por el almacenamiento de documentos de MongoDB.

---

## 🛠️ Tecnologías (Tech Stack)

QorA-A utiliza un enfoque de **Persistencia Políglota** para garantizar la escalabilidad y velocidad:

| Componente | Tecnología | Rol |
| :--- | :--- | :--- |
| **Backend** | [Django 5.2.7](https://www.djangoproject.com/) | Framework web robusto para la lógica central y la API. |
| **BD Relacional** | [PostgreSQL](https://www.postgresql.org/) | Almacenamiento principal para datos estructurados (Usuarios, Publicaciones). |
| **BD de Documentos** | [MongoDB](https://www.mongodb.com/) | Almacenamiento para datos semi-estructurados como análisis y registros. |
| **BD de Grafos** | [Neo4j](https://neo4j.com/) | Gestión de relaciones complejas muchos-a-muchos y lógica de recomendaciones. |
| **Caché y Cola de Tareas** | [Redis](https://redis.io/) | Caché de alta velocidad, gestión de sesiones y señales para tareas en segundo plano. |
| **Estilos** | Vanilla CSS | Diseño personalizado y responsivo para una experiencia de usuario (UI) premium. |

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
- Python 3.9+
- PostgreSQL
- MongoDB
- Neo4j
- Redis

---

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Josemaa13/QorA-A.git
   cd QorA-A
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración del Entorno:**
    Copia el archivo `.env.example` a `.env` y configura tus credenciales:
    ```bash
    cp .env.example .env
    ```
    Edita el archivo `.env` con tus credenciales reales de base de datos.

5. **Configurar Servicios de Base de Datos:**
    Asegúrate de tener PostgreSQL, MongoDB, Neo4j y Redis ejecutándose antes de continuar.

6. **Ejecutar Migraciones:**
    ```bash
    python manage.py migrate
    ```

7. **Crear Superusuario (Opcional):**
    ```bash
    python manage.py createsuperuser
    ```

8. **Recolectar Archivos Estáticos:**
    ```bash
    python manage.py collectstatic
    ```

9. **Iniciar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```

---

## 🛠️ Desarrollo

### Ejecutar Pruebas
```bash
python manage.py test
```

### Verificar el Estado del Proyecto
```bash
python manage.py check
```

### Crear Migraciones
```bash
python manage.py makemigrations
```

### Limpiar Cache de Python
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

---

## 📁 Estructura del Proyecto

- `apps/`: Contiene módulos de aplicación aislados (analytics, notifications, publications, etc.).
- `core/`: Configuración del proyecto, enrutamiento de URLs y gestores de servicios para MongoDB, Neo4j y Redis.
- `static/`: Recursos del frontend, incluyendo CSS y JavaScript.
- `templates/`: Estructuras HTML utilizando el motor de plantillas de Django.
- `media/`: Contenido subido por los usuarios.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
